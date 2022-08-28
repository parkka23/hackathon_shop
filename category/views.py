from django.shortcuts import render
from rest_framework import generics, permissions
from . import serializers
from .models import Category
from rest_framework.viewsets import ModelViewSet
from . import serializers
from rest_framework.decorators import action

# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.all()
    
    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return serializers.CategorySerializer
        elif self.action in ('create','update','partial_update'):
            return serializers.CategoryCreateSerializer
        else:
            return serializers.CategoryListSerializer
        
    def get_permissions(self):
        if self.action in ('create','update','partial_update','destroy'):
            return [permissions.IsAuthenticated(),permissions.IsAdminUser()]
        else:
            return [permissions.AllowAny()]

