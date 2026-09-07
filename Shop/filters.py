from django_filters.rest_framework import FilterSet
from .models import Product

class PriceFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "price": ["iexact" ,"gte" , "lte" , "range"],
        }