from rest_framework import serializers
from .models import Product, Comment, Like, ProductImages, Favourites
from django.db.models import Avg


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImages
        exclude=('id',)


class CommentSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Comment
        fields=('id','body','owner','product')

class LikeSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Like
        fields=('owner',)


class ProductListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Product
        fields=('id','title','price','preview')

    def to_representation(self, instance):
        repr= super().to_representation(instance)
        repr['rating']=instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr
        
class ProductDetailSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source='owner.username')
    images=ProductImageSerializer(many=True)

    def is_liked(self, product):
        user=self.context.get('request').user
        return user.liked.filter(product=product).exists()

    class Meta:
        model=Product
        fields='__all__'

    def to_representation(self, instance):
        repr= super().to_representation(instance)
        repr['likes']=instance.likes.count()
        repr['comments']=CommentSerializer(instance.comments.all(), many=True).data
        repr['rating']=instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews']=instance.reviews.count()
        return repr

class ProductCreateSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source='owner.username')

    images=ProductImageSerializer(many=True, read_only=False, required=False)

    class Meta:
        model=Product
        fields=('title','description','owner','price','category','preview','images')

    def create(self, validated_data):
        request=self.context.get('request')
        created_product=Product.objects.create(**validated_data)
        images_data=request.FILES
        images_object=[ProductImages(product=created_product, image=image) for image in images_data.getlist('images')]
        ProductImages.objects.bulk_create(images_object)
        return created_product



class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favourites
        fields=('product',)

    def to_representation(self, instance):
        repr= super().to_representation(instance)
        repr['product']=ProductListSerializer(instance.product).data
        return repr
    