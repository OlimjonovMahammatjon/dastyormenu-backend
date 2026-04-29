"""Organization serializers."""
import base64
import requests
from rest_framework import serializers
from django.conf import settings
from .models import Organization


def upload_logo_to_imgbb(image_file):
    """Upload logo to ImgBB and return URL."""
    try:
        # Read and encode image
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        
        # Upload to ImgBB
        payload = {
            'key': settings.IMGBB_API_KEY,
            'image': encoded_image,
            'name': image_file.name
        }
        
        response = requests.post(settings.IMGBB_API_URL, data=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('success'):
            return result['data']['url']
        else:
            raise serializers.ValidationError(f"ImgBB upload failed: {result}")
            
    except requests.exceptions.RequestException as e:
        raise serializers.ValidationError(f"Failed to upload logo: {str(e)}")
    except Exception as e:
        raise serializers.ValidationError(f"Logo upload error: {str(e)}")


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model."""
    
    is_trial_expired = serializers.ReadOnlyField()
    is_subscription_active = serializers.ReadOnlyField()
    logo_file = serializers.ImageField(write_only=True, required=False, help_text='Upload logo file')
    logo = serializers.URLField(read_only=True)
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'logo', 'logo_file', 'address', 'phone',
            'subscription_plan', 'subscription_status',
            'subscription_expires_at', 'trial_ends_at',
            'monthly_price', 'is_trial_expired',
            'is_subscription_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'logo']
    
    def create(self, validated_data):
        """Create organization with ImgBB logo upload."""
        logo_file = validated_data.pop('logo_file', None)
        
        # Upload logo to ImgBB if provided
        if logo_file:
            validated_data['logo'] = upload_logo_to_imgbb(logo_file)
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update organization with ImgBB logo upload."""
        logo_file = validated_data.pop('logo_file', None)
        
        # Upload new logo to ImgBB if provided
        if logo_file:
            validated_data['logo'] = upload_logo_to_imgbb(logo_file)
        
        return super().update(instance, validated_data)
    
    def validate_phone(self, value: str) -> str:
        """Validate phone number format."""
        if value and not value.replace('+', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Invalid phone number format")
        return value


class OrganizationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for organization list."""
    
    class Meta:
        model = Organization
        fields = ['id', 'name', 'logo', 'subscription_plan', 'subscription_status']
