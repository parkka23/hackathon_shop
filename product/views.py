from django.shortcuts import render
from . import serializers
from .models import Product, Comment, Like, Favourites
from rating.serializers import ReviewSerializer
from rest_framework import permissions, response, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .permissions import IsOwner
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


# Create your views here.
class StandartResultPagination(PageNumberPagination):
    page_size=5 
    page_query_param='page' 
    max_page_size=1000

class ProductViewSet(ModelViewSet):
    pagination_class=StandartResultPagination
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends=(DjangoFilterBackend,SearchFilter)
    filterset_fields=('category','owner')
    search_fields=('title',)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return serializers.ProductDetailSerializer
        elif self.action in ('create','update','partial_update'):
            return serializers.ProductCreateSerializer
        else:
            return serializers.ProductListSerializer

    def get_permissions(self):
        if self.action in ('create',):
            return [permissions.IsAuthenticated()]
        elif self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsOwner()]
        else:
            return [permissions.AllowAny()]

    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        if request.method == 'GET':
            reviews = product.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return response.Response(serializer, status=200)
        data = request.data
        serializer = ReviewSerializer(
            data=data, context={'request': request, 'product': product})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=201)

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        product = self.get_object()
        comments = product.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return response.Response(serializer.data, status=200)
    
    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        product=self.get_object()
        if request.user.liked.filter(product=product).exists():
            # delete like 1 method
            request.user.liked.filter(product=product).delete()
            return response.Response('You deleted the like', status=204)
        Like.objects.create(product=product, owner=request.user)
        return response.Response('You liked the post', status=201)

    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        product=self.get_object()
        likes=product.likes.all()
        serializer=serializers.LikeSerializer(likes, many=True)
        return response.Response(serializer.data, status=200)

    @action(['POST'], detail=True)
    def favourite_action(self, request, pk):
        product=self.get_object()
        if request.user.favourites.filter(product=product).exists():
            request.user.favourites.filter(product=product).delete()
            return response.Response('This post is deleted from Favourites', status=204)
        Favourites.objects.create(product=product, owner=request.user)
        return response.Response('This post is added to Favourites', status=201)

    


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwner)

