from django.db import models

from apps.clients.models import Client
from common.models import BaseModel


class Cart(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    variant = models.ForeignKey('products.Variant', on_delete=models.CASCADE, related_name='variant_cart', null=True)
    article = models.ForeignKey('products.Article', on_delete=models.CASCADE, related_name='article_cart', null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)