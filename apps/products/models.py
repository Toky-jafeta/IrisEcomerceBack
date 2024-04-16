from django.db import models

from apps.pictures.models import Pictures
from common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)


class Product(BaseModel):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    is_active = models.BooleanField(default=True)


class Article(BaseModel):
    name = models.CharField(max_length=50, null=True)
    price = models.DecimalField(decimal_places=3, max_digits=10, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='articles', null=True)
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    article_pictures = models.ManyToManyField(Pictures, default=None, blank=True, related_name='article_picture')


class Variant(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='variants', null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(decimal_places=3, max_digits=10)
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    variant_pictures = models.ManyToManyField(Pictures, default=None, blank=True)

