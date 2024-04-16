from rest_framework.viewsets import ModelViewSet

from apps.carts.models import Cart, CartItem
from apps.carts.serializers import CartSerializers, CartItemSerializers


class CartViewset(ModelViewSet):
    serializer_class = CartSerializers
    queryset = Cart.objects.all()


class CartItemViewset(ModelViewSet):
    serializer_class = CartItemSerializers
    queryset = CartItem.objects.all()