from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length= 100)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=255)
    description = models.TextField(blank = True , null = True)
    price = models.DecimalField(
                                validators = [MinValueValidator(1.00)],
                                max_digits = 10,
                                decimal_places = 2,
                                db_index=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"{self.name} - {self.price}"


class Cart(models.Model):

    user = models.OneToOneField(User , on_delete= models.CASCADE)

    def __str__(self):
        return f"{self.user} cart"  


class CartItem(models.Model):

    user = models.ForeignKey(User , on_delete= models.CASCADE)
    product = models.ForeignKey(
        Product , 
        on_delete= models.SET_NULL , 
        null=True , 
        related_name="cart_items")

    cart = models.ForeignKey(Cart , on_delete= models.SET_NULL , null =True)
    quantity = models.PositiveIntegerField(validators = [MinValueValidator(1)])

    def __str__(self):
        return f"{self.user} has {self.product} in his cart"

class Order(models.Model):

    user = models.ForeignKey(User , on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.user} order created at {self.created_at}"

class OrderItem(models.Model):

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name="order_items")
    product = models.ForeignKey(Product , on_delete= models.CASCADE , related_name="order_products")
    quantity = models.PositiveIntegerField(validators = [MinValueValidator(1)])
    price = models.DecimalField(
                                validators = [MinValueValidator(1.00)],
                                max_digits = 10,
                                decimal_places = 2)

    def __str__(self):
        return f"{self.user} - {self.order}"
