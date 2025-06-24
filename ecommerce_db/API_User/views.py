from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Category, ProductImage, User, Review
from .serializers import (
    ProductSerializer, CategorySerializer, ProductImageSerializer, 
    UserSerializer, ReviewSerializer, ProductDetailSerializer, UserDetailSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer  # Use detailed serializer for single product
        return ProductSerializer

    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        """Get all images for a specific product"""
        product = self.get_object()
        images = product.images.all()
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific product"""
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer  # Use detailed serializer for single user
        return UserSerializer

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews by a specific user"""
        user = self.get_object()
        reviews = user.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        queryset = Review.objects.all()
        product_id = self.request.query_params.get('product_id', None)
        user_id = self.request.query_params.get('user_id', None)
        
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
            
        return queryset