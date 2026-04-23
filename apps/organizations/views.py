"""Organization views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Organization
from .serializers import OrganizationSerializer, OrganizationListSerializer
from apps.users.permissions import IsSuperAdmin


class OrganizationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing organizations."""
    
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return OrganizationListSerializer
        return OrganizationSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        user = self.request.user
        if hasattr(user, 'userprofile'):
            if user.userprofile.role == 'super_admin':
                return Organization.objects.all()
            return Organization.objects.filter(id=user.userprofile.organization_id)
        return Organization.objects.none()
    
    @action(detail=True, methods=['post'])
    def activate_subscription(self, request, pk=None):
        """Activate organization subscription."""
        organization = self.get_object()
        organization.subscription_status = True
        organization.save(update_fields=['subscription_status'])
        return Response({'status': 'subscription activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate_subscription(self, request, pk=None):
        """Deactivate organization subscription."""
        organization = self.get_object()
        organization.subscription_status = False
        organization.save(update_fields=['subscription_status'])
        return Response({'status': 'subscription deactivated'})
