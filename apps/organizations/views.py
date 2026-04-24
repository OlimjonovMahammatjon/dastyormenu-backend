"""Organization views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Organization
from .serializers import OrganizationSerializer, OrganizationListSerializer
from apps.users.permissions import IsSuperAdmin


class OrganizationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing organizations."""
    
    queryset = Organization.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_permissions(self):
        """
        Public access for list and retrieve.
        Authentication required for create, update, delete.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsSuperAdmin()]
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return OrganizationListSerializer
        return OrganizationSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        queryset = Organization.objects.all()
        
        # For authenticated users, apply role-based filtering
        if self.request.user.is_authenticated and hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.role == 'super_admin':
                return Organization.objects.all()
            elif self.request.user.userprofile.organization:
                return Organization.objects.filter(id=self.request.user.userprofile.organization_id)
        
        # For public access, return all organizations
        return queryset
    
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
