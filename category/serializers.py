from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('slug','name')

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('slug','name','description')

    def create(self, validated_data):
        created_category=Category.objects.create(**validated_data)
        return created_category