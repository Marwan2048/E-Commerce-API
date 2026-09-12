from django.urls import path
from .views import( ProductAPIView , ProductDetailAPIView , AddProductCartAPIView , ProductCartAPIView , RemoveProductCartAPIView 
                   , CheckoutAPIView , OrderHistoryAPIView
)
urlpatterns = [
    
    path("products/" , ProductAPIView.as_view()),
    path("products/<int:pk>/" , ProductDetailAPIView.as_view()),
    path("cart/products/<int:pk>/" , AddProductCartAPIView.as_view()),
    path("cart/products/" , ProductCartAPIView.as_view()),
    path("cart/products/<int:pk>/remove/" , RemoveProductCartAPIView.as_view()),
    path("checkout/" , CheckoutAPIView.as_view()),
    path("orders/" , OrderHistoryAPIView.as_view()),
    
]