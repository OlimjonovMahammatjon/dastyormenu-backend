"""Menu views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Category, Menu
from .serializers import CategorySerializer, MenuSerializer, MenuListSerializer
from .mixins import OrganizationMixin
from apps.users.permissions import IsManagerOrAbove


class CategoryViewSet(OrganizationMixin, viewsets.ModelViewSet):
    """ViewSet for managing categories."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsManagerOrAbove]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['sort_order', 'name', 'created_at']
    ordering = ['sort_order']


class MenuViewSet(OrganizationMixin, viewsets.ModelViewSet):
    """ViewSet for managing menu items."""
    
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated, IsManagerOrAbove]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description', 'ingredients']
    ordering_fields = ['sort_order', 'name', 'price', 'created_at']
    ordering = ['sort_order']
    
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
