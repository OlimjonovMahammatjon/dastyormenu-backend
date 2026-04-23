"""Order views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .models import Order
from .serializers import (
    OrderSerializer, OrderListSerializer,
    OrderStatusSerializer, PublicOrderSerializer
)
from apps.menu.mixins import OrganizationMixin
from apps.users.permissions import IsWaiterOrAbove, IsChefOrAbove


class OrderViewSet(OrganizationMixin, viewsets.ModelViewSet):
    """ViewSet for managing orders."""
    
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsWaiterOrAbove]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'table', 'waiter']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    def get_queryset(self):
        """Filter orders with date range support."""
        queryset = super().get_queryset()
        
        # Date filtering
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set waiter from table assignment."""
        table = serializer.validated_data.get('table')
        waiter = table.assigned_waiter if table else None
        serializer.save(
            organization=self.request.user.userprofile.organization,
            waiter=waiter
        )
    
    @extend_schema(
        request=OrderStatusSerializer,
        responses={200: OrderSerializer},
        description='Update order status'
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsChefOrAbove])
    def update_status(self, request, pk=None):
        """Update order status."""
        order = self.get_object()
        serializer = OrderStatusSerializer(data=request.data)
        
        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            order.status = new_status
            
            if new_status == 'completed':
                order.completed_at = timezone.now()
            
            order.save()
            return Response(OrderSerializer(order).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsChefOrAbove])
    def active(self, request):
        """Get active orders for kitchen."""
        queryset = self.get_queryset().filter(
            status__in=['pending', 'cooking', 'ready']
        )
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_tables(self, request):
        """Get orders for waiter's assigned tables."""
        user_profile = request.user.userprofile
        queryset = self.get_queryset().filter(
            waiter=user_profile,
            status__in=['pending', 'cooking', 'ready']
        )
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


# Public endpoints (no auth required)
@extend_schema(
    request=PublicOrderSerializer,
    responses={201: PublicOrderSerializer},
    description='Public endpoint for creating orders via QR code'
)
@api_view(['POST'])
@permission_classes([AllowAny])
def public_create_order(request):
    """Public endpoint for creating orders via QR code."""
    serializer = PublicOrderSerializer(data=request.data)
    
    if serializer.is_valid():
        order = serializer.save()
        return Response(
            PublicOrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[
        OpenApiParameter(name='order_id', description='Order ID', required=True, type=str, location=OpenApiParameter.PATH)
    ],
    responses={200: OpenApiResponse(description='Order status')},
    description='Public endpoint for checking order status'
)
@api_view(['GET'])
@permission_classes([AllowAny])
def public_order_status(request, order_id):
    """Public endpoint for checking order status."""
    try:
        order = Order.objects.get(id=order_id)
        return Response({
            'id': str(order.id),
            'status': order.status,
            'table_number': order.table.table_number,
            'total_amount': order.total_amount,
            'created_at': order.created_at
        })
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found', 'code': 'ORDER_NOT_FOUND'},
            status=status.HTTP_404_NOT_FOUND
        )
