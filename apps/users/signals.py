"""User signals."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from apps.organizations.models import Organization


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create UserProfile when User is created.
    
    NOTE: This only works if organization exists.
    For admin panel, you should use UserProfileInline instead.
    """
    if created and not hasattr(instance, 'userprofile'):
        # Determine role based on user permissions
        if instance.is_superuser:
            role = 'super_admin'
            organization = None  # Super admin doesn't need organization
        elif instance.is_staff:
            role = 'manager'
            organization = Organization.objects.first()
        else:
            role = 'waiter'
            organization = Organization.objects.first()
        
        # Only create profile if organization exists (or super_admin)
        if organization or role == 'super_admin':
            UserProfile.objects.create(
                user=instance,
                organization=organization,
                full_name=instance.get_full_name() or instance.username,
                role=role,
                is_active=True
            )
