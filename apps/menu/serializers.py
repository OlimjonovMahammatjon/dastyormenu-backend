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
    
    class Meta:
        model = Menu
        fields = [
            'id', 'name', 'image_url', 'price',
            'category_name', 'is_available', 'cook_time_minutes'
        ]
