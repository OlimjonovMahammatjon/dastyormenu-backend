"""Menu serializers."""
import base64
import requests
from rest_framework import serializers
from django.conf import settings
from .models import Category, Menu


def upload_to_imgbb(image_file):
    """Upload image to ImgBB and return URL."""
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
        raise serializers.ValidationError(f"Failed to upload image: {str(e)}")
    except Exception as e:
        raise serializers.ValidationError(f"Image upload error: {str(e)}")


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'organization', 'name', 'icon',
            'sort_order', 'is_active', 'items_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'organization': {'required': False}
        }
    
    def get_items_count(self, obj) -> int:
        """Get count of items in category."""
        return obj.items.filter(is_available=True).count()


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for Menu model."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    price_uzs = serializers.ReadOnlyField()
    image = serializers.ImageField(write_only=True, required=False, help_text='Upload image file')
    image_url = serializers.URLField(read_only=True)
    
    class Meta:
        model = Menu
        fields = [
            'id', 'organization', 'category', 'category_name',
            'name', 'description', 'image', 'image_url', 'price', 'price_uzs',
            'cook_time_minutes', 'ingredients', 'is_available',
            'sort_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'image_url']
        extra_kwargs = {
            'organization': {'required': False}
        }
    
    def create(self, validated_data):
        """Create menu item with ImgBB image upload."""
        image_file = validated_data.pop('image', None)
        
        # Upload image to ImgBB if provided
        if image_file:
            validated_data['image_url'] = upload_to_imgbb(image_file)
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update menu item with ImgBB image upload."""
        image_file = validated_data.pop('image', None)
        
        # Upload new image to ImgBB if provided
        if image_file:
            validated_data['image_url'] = upload_to_imgbb(image_file)
        
        return super().update(instance, validated_data)
    
    def validate_price(self, value: int) -> int:
        """Validate price is positive."""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value
    
    def validate_cook_time_minutes(self, value: int) -> int:
        """Validate cook time is positive."""
        if value < 0:
            raise serializers.ValidationError("Cook time cannot be negative")
        return value


class MenuListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for menu list."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.UUIDField(source='category.id', read_only=True)
    price_uzs = serializers.ReadOnlyField()
    
    class Meta:
        model = Menu
        fields = [
            'id', 'name', 'description', 'image_url', 'price', 'price_uzs',
            'category_id', 'category_name', 'ingredients',
            'is_available', 'cook_time_minutes', 'sort_order'
        ]
