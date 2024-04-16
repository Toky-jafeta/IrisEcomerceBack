from rest_framework.serializers import ModelSerializer

from apps.carts.models import Cart, CartItem


class CartSerializers(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializers(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'