from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny , IsAdminUser
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from .models import Product 
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