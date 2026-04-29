"""Menu serializers."""
from rest_framework import serializers
from .models import Category, Menu


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
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = [
            'id', 'organization', 'category', 'category_name',
            'name', 'description', 'image_url', 'price', 'price_uzs',
            'cook_time_minutes', 'ingredients', 'is_available',
            'sort_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'organization': {'required': False}
        }
    
    def get_image_url(self, obj):
        """Get full image URL (Cloudinary or local)."""
        if obj.image_url:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image_url.url)
            return obj.image_url.url
        return None
    
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
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = [
            'id', 'name', 'description', 'image_url', 'price', 'price_uzs',
            'category_id', 'category_name', 'ingredients',
            'is_available', 'cook_time_minutes', 'sort_order'
        ]
    
    def get_image_url(self, obj):
        """Get full image URL (Cloudinary or local)."""
        if obj.image_url:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image_url.url)
            return obj.image_url.url
        return None
