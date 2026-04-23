"""User views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import UserProfile
from .serializers import (
    UserProfileSerializer, SetPinSerializer,
    LoginSerializer, PinLoginSerializer
)
from .permissions import IsManagerOrAbove


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user profiles."""
    
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAbove]
    
    def get_queryset(self):
        """Filter users by organization."""
        user = self.request.user
        if hasattr(user, 'userprofile'):
            if user.userprofile.role == 'super_admin':
                return UserProfile.objects.all()
            return UserProfile.objects.filter(
                organization=user.userprofile.organization
            )
        return UserProfile.objects.none()
    
    def perform_create(self, serializer):
        """Set organization from current user."""
        if not serializer.validated_data.get('organization'):
            serializer.save(organization=self.request.user.userprofile.organization)
        else:
            serializer.save()
    
    @extend_schema(
        request=SetPinSerializer,
        responses={200: OpenApiResponse(description='PIN set successfully')}
    )
    @action(detail=True, methods=['post'])
    def set_pin(self, request, pk=None):
        """Set PIN code for user."""
        user_profile = self.get_object()
        serializer = SetPinSerializer(data=request.data)
        
        if serializer.is_valid():
            user_profile.set_pin(serializer.validated_data['pin_code'])
            user_profile.save()
            return Response({'status': 'PIN set successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
    request=LoginSerializer,
    responses={200: UserProfileSerializer},
    description='Login with username/email and password'
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login with username/email and password."""
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    login_input = serializer.validated_data['login']
    password = serializer.validated_data['password']
    
    # Try to authenticate with username first
    user = authenticate(username=login_input, password=password)
    
    # If failed, try with email
    if not user:
        try:
            from django.contrib.auth.models import User
            user_obj = User.objects.get(email=login_input)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass
    
    if not user:
        return Response(
            {'error': 'Invalid credentials', 'code': 'INVALID_CREDENTIALS'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not hasattr(user, 'userprofile'):
        return Response(
            {'error': 'User profile not found', 'code': 'PROFILE_NOT_FOUND'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'user': UserProfileSerializer(user.userprofile).data
    })


@extend_schema(
    request=PinLoginSerializer,
    responses={200: UserProfileSerializer},
    description='PIN login endpoint for chefs and waiters'
)
@api_view(['POST'])
@permission_classes([AllowAny])
def pin_login_view(request):
    """PIN login endpoint for chefs and waiters."""
    serializer = PinLoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    organization_id = serializer.validated_data['organization_id']
    pin_code = serializer.validated_data['pin_code']
    
    # Find user by organization and PIN
    profiles = UserProfile.objects.filter(
        organization_id=organization_id,
        is_active=True
    ).exclude(pin_code='')
    
    for profile in profiles:
        if profile.check_pin(pin_code):
            refresh = RefreshToken.for_user(profile.user)
            return Response({
                'access_token': str(refresh.access_token),
                'user': UserProfileSerializer(profile).data
            })
    
    return Response(
        {'error': 'Invalid PIN or organization', 'code': 'INVALID_PIN'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@extend_schema(
    request=None,
    responses={200: OpenApiResponse(description='Logged out successfully')},
    description='Logout endpoint'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout endpoint."""
    return Response({'status': 'logged out successfully'})
