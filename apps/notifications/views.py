"""Notification views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing notifications."""
    
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_permissions(self):
        """
        Public access for list and retrieve.
        Authentication required for mark_read and mark_all_read.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter notifications."""
        queryset = Notification.objects.all()
        
        # Filter by organization_id if provided
        organization_id = self.request.query_params.get('organization_id')
        if organization_id:
            queryset = queryset.filter(recipient__organization_id=organization_id)
        
        # Filter by recipient_id if provided
        recipient_id = self.request.query_params.get('recipient_id')
        if recipient_id:
            queryset = queryset.filter(recipient_id=recipient_id)
        
        # For authenticated users, filter by current user
        if self.request.user.is_authenticated and hasattr(self.request.user, 'userprofile'):
            queryset = queryset.filter(recipient=self.request.user.userprofile)
        
        return queryset
    
    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(description='Marked as read')},
        description='Mark notification as read'
    )
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read."""
        notification = self.get_object()
        notification.mark_read()
        return Response({'status': 'marked as read'})
    
    @extend_schema(
        request=None,
        responses={200: OpenApiResponse(description='All marked as read')},
        description='Mark all notifications as read'
    )
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read."""
        self.get_queryset().update(is_read=True)
        return Response({'status': 'all marked as read'})
