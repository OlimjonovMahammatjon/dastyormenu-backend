"""Organization serializers."""
from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model."""
    
    is_trial_expired = serializers.ReadOnlyField()
    is_subscription_active = serializers.ReadOnlyField()
    logo = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'logo', 'address', 'phone',
            'subscription_plan', 'subscription_status',
            'subscription_expires_at', 'trial_ends_at',
            'monthly_price', 'is_trial_expired',
            'is_subscription_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_logo(self, obj):
        """Get full logo URL (Cloudinary or local)."""
        if obj.logo:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
    
    def validate_phone(self, value: str) -> str:
        """Validate phone number format."""
        if value and not value.replace('+', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Invalid phone number format")
        return value


class OrganizationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for organization list."""
    
    logo = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = ['id', 'name', 'logo', 'subscription_plan', 'subscription_status']
    
    def get_logo(self, obj):
        """Get full logo URL (Cloudinary or local)."""
        if obj.logo:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
