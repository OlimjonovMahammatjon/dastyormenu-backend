"""Table views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Table
from .serializers import TableSerializer, TableListSerializer
from apps.menu.mixins import OrganizationMixin
from apps.users.permissions import IsManagerOrAbove


class TableViewSet(OrganizationMixin, viewsets.ModelViewSet):
    """ViewSet for managing tables."""
    
    queryset = Table.objects.all()
    permission_classes = [IsAuthenticated, IsManagerOrAbove]
    
    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'list':
            return TableListSerializer
        return TableSerializer
    
    @action(detail=True, methods=['get'])
    def qr_code(self, request, pk=None):
        """Download QR code image."""
        table = self.get_object()
        
        if not table.qr_code_image:
            return Response(
                {'error': 'QR code not generated', 'code': 'QR_NOT_FOUND'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        response = HttpResponse(table.qr_code_image.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="table_{table.table_number}_qr.png"'
        return response
    
    @extend_schema(
        request=None,
        responses={200: TableSerializer},
        description='Regenerate QR code for table'
    )
    @action(detail=True, methods=['post'])
    def regenerate_qr(self, request, pk=None):
        """Regenerate QR code for table."""
        table = self.get_object()
        table.regenerate_qr_code()
        serializer = self.get_serializer(table)
        return Response(serializer.data)
