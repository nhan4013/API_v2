from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from .models import Product, Category, ProductImage, User, Review
from API_User.services import recommendation_service
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
        serializer = ProductImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific product"""
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def similar_products(self, request, pk=None):
        """Get similar products using KNN model"""
        try:
            product_id = pk
            num_similar = int(request.query_params.get('limit', 5))
            
            similar_products = recommendation_service.get_similar_products(
                product_id=product_id, 
                num_similar=num_similar
            )
            
            result = []
            for item in similar_products:
                result.append({
                    'product_id': item['product_id'],
                    'product_name': item['product_name'],
                    'product_price': item['product_price'],
                    'similarity_score': round(item['similarity_score'], 2),
                    'based_on_users': item['based_on_users']
                })
            
            return Response({
                'target_product_id': product_id,
                'model_used': 'KNN',
                'similar_products': result
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

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
        serializer = UserDetailSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        """Get personalized recommendations for a user using SVD++"""
        try:
            user_id = pk
            num_recommendations = int(request.query_params.get('limit', 10))
            recommendation_type = request.query_params.get('type', 'personalized')
            
            if recommendation_type == 'hybrid':
                recommendations = recommendation_service.get_hybrid_recommendations(
                    user_id=user_id, 
                    num_recommendations=num_recommendations
                )
            else:
                recommendations = recommendation_service.get_personalized_recommendations(
                    user_id=user_id, 
                    num_recommendations=num_recommendations
                )
            
            result = []
            for rec in recommendations:
                result.append({
                    'product_id': rec['product_id'],
                    'product_name': rec['product_name'],
                    'product_price': rec['product_price'],
                    'predicted_rating': round(rec['predicted_rating'], 2),
                    'recommendation_type': rec.get('recommendation_type', 'personalized'),
                    'rank': rec.get('rank', 0)
                })
            
            return Response({
                'user_id': user_id,
                'model_used': 'SVD++' if recommendation_type != 'hybrid' else 'Hybrid (SVD++ + KNN)',
                'recommendation_type': recommendation_type,
                'total_recommendations': len(result),
                'recommendations': result
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

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

# Legacy function-based views (kept for backward compatibility)
def get_recommendations(request, user_id):
    """API endpoint to get personalized recommendations for a user (SVD++)"""
    try:
        num_recommendations = int(request.GET.get('limit', 10))
        recommendation_type = request.GET.get('type', 'personalized')
        
        if recommendation_type == 'hybrid':
            recommendations = recommendation_service.get_hybrid_recommendations(
                user_id=user_id, 
                num_recommendations=num_recommendations
            )
            model_used = 'Hybrid (SVD++ + KNN)'
        else:
            recommendations = recommendation_service.get_personalized_recommendations(
                user_id=user_id, 
                num_recommendations=num_recommendations
            )
            model_used = 'SVD++'
        
        result = []
        for rec in recommendations:
            result.append({
                'product_id': rec['product_id'],
                'product_name': rec['product_name'],
                'product_price': rec['product_price'],
                'predicted_rating': round(rec['predicted_rating'], 2),
                'recommendation_type': rec.get('recommendation_type', 'personalized')
            })
        
        return JsonResponse({
            'user_id': user_id,
            'model_used': model_used,
            'total_recommendations': len(result),
            'recommendations': result
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_similar_products(request, product_id):
    """API endpoint to get similar products using KNN"""
    try:
        num_similar = int(request.GET.get('limit', 5))
        
        similar_products = recommendation_service.get_similar_products(
            product_id=product_id, 
            num_similar=num_similar
        )
        
        result = []
        for item in similar_products:
            result.append({
                'product_id': item['product_id'],
                'product_name': item['product_name'],
                'product_price': item['product_price'],
                'similarity_score': round(item['similarity_score'], 2),
                'based_on_users': item['based_on_users']
            })
        
        return JsonResponse({
            'target_product_id': product_id,
            'model_used': 'KNN',
            'similar_products': result
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def predict_rating(request, user_id, product_id):
    """API endpoint to predict rating for user-product pair"""
    try:
        model_type = request.GET.get('model', 'svdpp')  # 'svdpp' or 'knn'
        use_svdpp = model_type.lower() == 'svdpp'
        
        prediction = recommendation_service.predict_user_product_rating(
            user_id=user_id, 
            product_id=product_id, 
            use_svdpp=use_svdpp
        )
        
        if prediction:
            return JsonResponse(prediction)
        else:
            return JsonResponse({'error': 'Could not make prediction'}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['GET'])
def volume_status(request):
    """Check volume mount status"""
    status = recommendation_service.check_volume_status()
    return Response(status)

def compare_models(request, user_id, product_id):
    """Compare predictions from both models"""
    try:
        svdpp_prediction = recommendation_service.predict_user_product_rating(
            user_id=user_id, 
            product_id=product_id, 
            use_svdpp=True
        )
        
        knn_prediction = recommendation_service.predict_user_product_rating(
            user_id=user_id, 
            product_id=product_id, 
            use_svdpp=False
        )
        
        return JsonResponse({
            'user_id': user_id,
            'product_id': product_id,
            'svdpp_prediction': svdpp_prediction,
            'knn_prediction': knn_prediction,
            'difference': abs(svdpp_prediction['predicted_rating'] - knn_prediction['predicted_rating']) if svdpp_prediction and knn_prediction else None
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)