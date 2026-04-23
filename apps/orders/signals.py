"""Order signals."""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Order, OrderItem


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance: Order, created: bool, **kwargs):
    """Handle order status changes."""
    channel_layer = get_channel_layer()
    
    if created:
        # New order - notify kitchen
        async_to_sync(channel_layer.group_send)(
            f'org_{instance.organization_id}_kitchen',
            {
                'type': 'order_update',
                'order_id': str(instance.id),
                'status': instance.status,
                'table_number': instance.table.table_number,
                'action': 'new_order'
            }
        )
        
        # Create notification
        from apps.notifications.models import Notification
        Notification.objects.create(
            organization=instance.organization,
            recipient=instance.waiter if instance.waiter else None,
            type='new_order',
            message=f'New order from Table {instance.table.table_number}',
            order=instance
        )
    
    else:
        # Status changed
        if instance.status == 'cooking':
            # Notify kitchen
            async_to_sync(channel_layer.group_send)(
                f'org_{instance.organization_id}_kitchen',
                {
                    'type': 'order_update',
                    'order_id': str(instance.id),
                    'status': instance.status,
                    'action': 'status_changed'
                }
            )
        
        elif instance.status == 'ready':
            # Notify waiter
            if instance.waiter:
                async_to_sync(channel_layer.group_send)(
                    f'user_{instance.waiter.id}',
                    {
                        'type': 'notification',
                        'message': f'Order for Table {instance.table.table_number} is ready',
                        'order_id': str(instance.id)
                    }
                )
                
                from apps.notifications.models import Notification
                Notification.objects.create(
                    organization=instance.organization,
                    recipient=instance.waiter,
                    type='order_ready',
                    message=f'Order for Table {instance.table.table_number} is ready',
                    order=instance
                )
        
        elif instance.status == 'completed':
            # Create pending payment
            from apps.payments.models import Payment
            Payment.objects.get_or_create(
                order=instance,
                defaults={
                    'organization': instance.organization,
                    'amount': instance.total_with_tip,
                    'payment_status': 'pending'
                }
            )


@receiver(post_save, sender=OrderItem)
def snapshot_menu_data(sender, instance: OrderItem, created: bool, **kwargs):
    """Snapshot menu data when order item is created."""
    if created and instance.menu:
        if not instance.menu_name:
            instance.menu_name = instance.menu.name
        if not instance.menu_price:
            instance.menu_price = instance.menu.price
        instance.save(update_fields=['menu_name', 'menu_price'])
