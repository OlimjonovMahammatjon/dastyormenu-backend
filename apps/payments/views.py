"""Payment views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from .models import Payment
from .serializers import PaymentSerializer, PaymentConfirmSerializer
from apps.menu.mixins import OrganizationMixin
from apps.users.permissions import IsWaiterOrAbove


class PaymentViewSet(OrganizationMixin, viewsets.ModelViewSet):
    """ViewSet for managing payments."""
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_permissions(self):
        """
        Public access for list and retrieve.
        Authentication required for create, update, delete, confirm.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsWaiterOrAbove()]
    
    def get_queryset(self):
        """Filter payments."""
        queryset = Payment.objects.all()
        
        # Filter by organization_id if provided
        organization_id = self.request.query_params.get('organization_id')
        if organization_id:
            queryset = queryset.filter(order__organization_id=organization_id)
        
        # Filter by order_id if provided
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        
        # For authenticated users, filter by their organization
        if self.request.user.is_authenticated and hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.organization:
                queryset = queryset.filter(order__organization=self.request.user.userprofile.organization)
        
        return queryset
    
    @extend_schema(
        request=PaymentConfirmSerializer,
        responses={200: PaymentSerializer},
        description='Confirm payment'
    )
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm payment."""
        payment = self.get_object()
        serializer = PaymentConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            transaction_id = serializer.validated_data.get('transaction_id', '')
            payment.mark_paid(transaction_id)
            return Response(PaymentSerializer(payment).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
