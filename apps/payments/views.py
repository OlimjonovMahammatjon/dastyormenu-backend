"""Payment views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Payment
from .serializers import PaymentSerializer, PaymentConfirmSerializer
from apps.menu.mixins import OrganizationMixin
from apps.users.permissions import IsWaiterOrAbove


class PaymentViewSet(OrganizationMixin, viewsets.ModelViewSet):
    """ViewSet for managing payments."""
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsWaiterOrAbove]
    
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
