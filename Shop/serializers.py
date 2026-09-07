from rest_framework import serializers
from .models import Product , CartItem , Order , OrderItem , Category

class ProductSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        many = True ,
        slug_field = "name",
        queryset = Category.objects.all()
    )
    stock = serializers.IntegerField(write_only = True)
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "stock",
            "image"
        ]

class CartItemSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = CartItem     
        fields = [
            "id",
            "user",
            "product",
            "quantity"
        ]

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "created_at"
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    order = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "user",
            "order",
            "product",
            "quantity",
            "price"
        ]