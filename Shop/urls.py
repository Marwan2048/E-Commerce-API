from django.urls import path
from .views import ProductAPIView , ProductDetailAPIView , AddProductCartAPIView

urlpatterns = [
    
    path("products/" , ProductAPIView.as_view()),
    path("products/<int:pk>/" , ProductDetailAPIView.as_view()),
    path("cart/products/<int:pk>/" , AddProductCartAPIView.as_view()),
    
    
]