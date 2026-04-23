"""Public menu views (no authentication required)."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.tables.models import Table
from .models import Menu
from .serializers import MenuListSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='qr', description='QR code ID', required=True, type=str)
    ],
    responses={200: MenuListSerializer(many=True)},
    description='Public endpoint for viewing menu via QR code'
)
@api_view(['GET'])
@permission_classes([AllowAny])
def public_menu(request):
    """Public endpoint for viewing menu via QR code."""
    qr_code_id = request.query_params.get('qr')
    
    if not qr_code_id:
        return Response(
            {'error': 'QR code ID required', 'code': 'QR_REQUIRED'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        table = Table.objects.select_related('organization').get(qr_code_id=qr_code_id)
    except Table.DoesNotExist:
        return Response(
            {'error': 'Invalid QR code', 'code': 'INVALID_QR'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get available menu items
    menu_items = Menu.objects.filter(
        organization=table.organization,
        is_available=True
    ).select_related('category').order_by('sort_order')
    
    serializer = MenuListSerializer(menu_items, many=True)
    
    return Response({
        'organization': {
            'id': str(table.organization.id),
            'name': table.organization.name,
            'logo': table.organization.logo.url if table.organization.logo else None,
        },
        'table': {
            'id': str(table.id),
            'number': table.table_number,
            'qr_code_id': str(table.qr_code_id)
        },
        'menu': serializer.data
    })
