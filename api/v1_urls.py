from django.urls import re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers

from apps.carts.views import CartViewset, CartItemViewset
from apps.clients.views import ClientViewset
from apps.pictures.views import PicturesViewset
from apps.products.views import CategoryViewset, ProductViewset, ArticleViewset, VariantViewset
from apps.users.views import UserViewset

app_name = 'api-ecommerce'

router = DefaultRouter()

router.register('user', UserViewset, basename='user')
router.register('category', CategoryViewset, basename='product-category')
router.register('products', ProductViewset, basename='product')
router.register('articles', ArticleViewset, basename='articles')

article_router = routers.NestedSimpleRouter(router, r'articles', lookup='articles')
article_router.register(r'variants', VariantViewset, basename='variants')

router.register('client', ClientViewset, basename='client')
router.register('pictures', PicturesViewset, basename='pictures')

router.register('cart', CartViewset, basename='cart')

cart_router = routers.NestedSimpleRouter(router, r'cart', lookup='cart')
cart_router.register(r'cartitems', CartItemViewset, basename='cartitems')


urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^', include(article_router.urls)),
    re_path(r'^token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]