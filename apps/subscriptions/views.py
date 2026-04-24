"""Subscription views."""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Subscription
from .serializers import SubscriptionSerializer
from apps.users.permissions import IsManagerOrAbove


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing subscriptions."""
    
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    
    def get_permissions(self):
        """
        Public access for list and retrieve.
        Authentication required for current and history.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsManagerOrAbove()]
    
    def get_queryset(self):
        """Filter subscriptions."""
        queryset = Subscription.objects.all()
        
        # Filter by organization_id if provided
        organization_id = self.request.query_params.get('organization_id')
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        
        # For authenticated users, filter by their organization
        if self.request.user.is_authenticated and hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.organization:
                queryset = queryset.filter(organization=self.request.user.userprofile.organization)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current subscription info."""
        user = request.user
        if hasattr(user, 'userprofile'):
            org = user.userprofile.organization
            return Response({
                'plan': org.subscription_plan,
                'status': org.subscription_status,
                'expires_at': org.subscription_expires_at,
                'trial_ends_at': org.trial_ends_at,
                'is_active': org.is_subscription_active
            })
        return Response({'error': 'User profile not found'}, status=404)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get subscription payment history."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
