from django.shortcuts import render , get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView , ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer , CartItemSerializer , OrderSerializer
from .models import Product , CartItem , Cart , OrderItem , Order
from .filters import PriceFilter

# Create your views here.


class ProductAPIView(ListCreateAPIView):

    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_class = PriceFilter
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    search_fields = ["name"]
    ordering_fields = ["price"]

    def get_queryset(self):
        return Product.objects.filter(stock__gt = 0
                                ).prefetch_related("category")

    def get_permissions(self):

        if self.request.method == "GET":
            self.permission_classes = [AllowAny]

        elif self.request.method == "POST":
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):

        if self.request.method == "GET":
            return Product.objects.filter(stock__gt = 0
                                    ).prefetch_related("category")

        elif self.request.method in ("PUT" , "PATCH" , "DELETE"):
            return Product.objects.prefetch_related("category")
                                    
    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]

        elif self.request.method in ("PUT" , "PATCH" , "DELETE"):
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

class AddProductCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request , pk):
        product = get_object_or_404(Product , id = pk)
        cart = get_object_or_404(Cart , user = self.request.user)

        if CartItem.objects.filter(user = self.request.user , product = product).exists():
            cart_item = CartItem.objects.get(
                user = self.request.user ,
                product = product)
            
            cart_item.quantity += 1
            cart_item.save()

            return Response({
            "message": "quantity increased by 1"
            })

        CartItem.objects.create(
            user=self.request.user,
            product=product,
            cart=cart,
            quantity=1
        )

        return Response({
            "message": "product added to cart successfully"
        })

class RemoveProductCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request , pk):

        product = get_object_or_404(Product , id = pk)     
        cart_item_found = CartItem.objects.filter(user=self.request.user , product = product).exists()
        
        if cart_item_found:
            cart_item = CartItem.objects.get(user=self.request.user , product = product)

            if cart_item.quantity > 1 and cart_item:
                cart_item.quantity -= 1
                cart_item.save()
                return Response({
                            "message": "quantity decreased by 1"
                            })

            elif cart_item.quantity <= 1 and cart_item:
                cart_item.delete()
                return Response({
                            "message": "product removed from cart successfully"
                        })

        else:
            return Response({
                "message":"product not in cart"
            },status.HTTP_404_NOT_FOUND)


class ProductCartAPIView(ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user = self.request.user).select_related("product")


class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):

        cart_items = CartItem.objects.filter(user = self.request.user)
        order = Order.objects.create(user = self.request.user)

        for item in cart_items:
            OrderItem.objects.create(
                user = self.request.user,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price,
                order = order
            )

        cart_items.delete()

        return Response({
            "message" : "checkout is done"
        })

class OrderHistoryAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)