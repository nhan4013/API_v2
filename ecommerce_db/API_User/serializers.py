from rest_framework import serializers
from .models import Product, Category, ProductImage, User, Review

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url','id', 'name']

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url','id', 'small_url', 'medium_url', 'large_url', 'product']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['url','id', 'name', 'average_rating', 'description', 'price', 'images']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url','id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Don't expose password in responses
        }

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    product_id = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Review
        fields = ['url','id', 'title', 'content', 'timestamp', 'product', 'user', 'product_id', 'user_id']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        user_id = validated_data.pop('user_id')
        
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)
        
        review = Review.objects.create(
            product=product,
            user=user,
            **validated_data
        )
        return review

# Detailed serializers with nested relationships
class ProductDetailSerializer(serializers.HyperlinkedModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['url','id', 'name', 'average_rating', 'description', 'price', 'images', 'reviews']

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['url','id', 'username', 'reviews']
        extra_kwargs = {
            'password': {'write_only': True}
        }