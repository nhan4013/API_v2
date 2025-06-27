from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ProductImageViewSet, 
    UserViewSet, ReviewViewSet
)
from API_User import views

# Create a router and register our ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/<str:user_id>/', views.get_recommendations, name='get_recommendations'),
    path('predict/<str:user_id>/<str:product_id>/', views.predict_rating, name='predict_rating'),
    
    # New recommendation endpoints
    path('similar-products/<str:product_id>/', views.get_similar_products, name='get_similar_products'),
    path('compare-models/<str:user_id>/<str:product_id>/', views.compare_models, name='compare_models'),
]