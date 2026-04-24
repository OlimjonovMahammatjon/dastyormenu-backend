"""Menu views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .models import Category, Menu
from .serializers import CategorySerializer, MenuSerializer, MenuListSerializer
from .mixins import OrganizationMixin
from apps.users.permissions import IsManagerOrAbove


class CategoryViewSet(OrganizationMixin, viewsets.ModelViewSet):
    """ViewSet for managing categories."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['sort_order', 'name', 'created_at']
    ordering = ['sort_order']
    
    def get_permissions(self):
        """
        Public access for list and retrieve.
        Authentication required for create, update, delete.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsManagerOrAbove()]
    
    def get_queryset(self):
        """Filter by organization if provided."""
        queryset = Category.objects.all()
        
        # Filter by organization_id if provided
        organization_id = self.request.query_params.get('organization_id')
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        
        # For authenticated users, filter by their organization
        elif self.request.user.is_authenticated and hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.organization:
                queryset = queryset.filter(organization=self.request.user.userprofile.organization)
        
        return queryset


class MenuViewSet(OrganizationMixin, viewsets.ModelViewSet):
    """ViewSet for managing menu items."""
    
    queryset = Menu.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description', 'ingredients']
    ordering_fields = ['sort_order', 'name', 'price', 'created_at']
    ordering = ['sort_order']
    
    def get_permissions(self):
        """
        Public access for list and retrieve.
        Authentication required for create, update, delete.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsManagerOrAbove()]
    
    def get_queryset(self):
        """Filter by organization if provided."""
        queryset = Menu.objects.all()
        
        # Filter by organization_id if provided
        organization_id = self.request.query_params.get('organization_id')
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        
        # Filter by category_id if provided
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # For authenticated users, filter by their organization
        elif self.request.user.is_authenticated and hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.organization:
                queryset = queryset.filter(organization=self.request.user.userprofile.organization)
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'list':
            return MenuListSerializer
        return MenuSerializer
    
    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(description='Availability toggled')},
        description='Toggle menu item availability (stop-list)'
    )
    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        """Toggle menu item availability (stop-list)."""
        menu_item = self.get_object()
        menu_item.toggle_availability()
        return Response({
            'status': 'availability toggled',
            'is_available': menu_item.is_available
        })
