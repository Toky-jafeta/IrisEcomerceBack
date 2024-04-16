import base64
from base64 import b64encode
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Min
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound


from apps.pictures.models import Pictures
from apps.products.models import Category, Product, Article, Variant
from apps.products.serializers import CategorySerializers, ProductSerializers, ArticleSerializers, \
    MinimalListCategorySerializers, MinimalListProductSerializers, VariantSerializers, MinimalListArticleSerializers, \
    MinimalListVariantSerializers, MinimalRetriveArticleSerializers


class CategoryViewset(ModelViewSet):
    serializer_class = CategorySerializers
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, last_author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_author=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return MinimalListCategorySerializers
        return super().get_serializer_class()


class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializers
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, last_author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_author=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return MinimalListProductSerializers
        return super().get_serializer_class()


class ArticleViewset(ModelViewSet):
    serializer_class = ArticleSerializers
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, last_author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_author=self.request.user)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'minimal_price':
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return MinimalListArticleSerializers
        elif self.action == 'retrieve':
            return MinimalRetriveArticleSerializers
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        pictures_data = []
        if "article_pictures" in request.data:
            pictures_data = request.data.pop("article_pictures")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        article = Article.objects.get(id=serializer.data.get('id'))

        if pictures_data:
            for picture_file in pictures_data:
                picture_name = picture_file.name
                picture_extension = picture_name.split(".")[-1]
                picture_content = b64encode(picture_file.read()).decode("utf-8")
                picture = Pictures.objects.create(
                    name=picture_name, extention=picture_extension, content=picture_content
                )
                article.article_pictures.add(picture.id)
                article.save()
        return Response(ArticleSerializers(article).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data_dict = dict(request.data)
        pictures_data = data_dict.pop("article_pictures", None)
        serializer = self.get_serializer(instance, data=data_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        article = self.get_object()

        if pictures_data:
            picture_ids = [picture.id for picture in article.article_pictures.all()]
            new_picture_id = []
            for item in pictures_data:
                try:
                    new_picture_id.append(int(item))
                    article.article_pictures.add(int(item))
                except:
                    picture_file = item
                    picture_name = picture_file.name
                    picture_extension = picture_name.split(".")[-1]
                    picture_content = base64.b64encode(picture_file.read()).decode("utf-8")
                    picture = Pictures.objects.create(
                        name=picture_name, extention=picture_extension, content=picture_content
                    )
                    new_picture_id.append(picture.id)
                    article.article_pictures.add(picture.id)
            picture_ids_to_remove = [id for id in picture_ids if id not in new_picture_id]

            article.article_pictures.remove(*picture_ids_to_remove)

        article.save()

        return Response(ArticleSerializers(article).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def minimal_price(self, request, *args, **kwargs):
        article_id = self.request.data.get('article_id')
        try:
            article = Article.objects.get(id=article_id)
            if article.variants.exists():
                min_price = article.variants.aggregate(min_price=Min('price'))['min_price']
                return Response({'minimal_price': Decimal(min_price)})
            else:
                raise NotFound("No variants found for this article")
        except Article.DoesNotExist:
            raise NotFound("Article does not exist")


class VariantViewset(ModelViewSet):
    serializer_class = VariantSerializers
    queryset = Variant.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, last_author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_author=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return MinimalListVariantSerializers
        return super().get_serializer_class()

    @action(methods=['post'], detail=False)
    def update_or_create_variants(self, request, *args, **kwargs):
        article_id = self.kwargs['articles_pk']
        existing_variants = Variant.objects.filter(article_id=article_id)
        existing_variant_ids = set(existing_variants.values_list('id', flat=True))
        updated_variants = []

        for variant_data in self.request.data:
            variant_id = variant_data.get('id')
            if variant_id in existing_variant_ids:
                variant = existing_variants.get(id=variant_id)
                serializer = VariantSerializers(instance=variant, data=variant_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_variants.append(serializer.data)
                existing_variant_ids.remove(variant_id)
            else:
                serializer = VariantSerializers(data={**variant_data, 'article': article_id})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_variants.append(serializer.data)

        if existing_variant_ids:
            Variant.objects.filter(id__in=existing_variant_ids).delete()

        return Response(updated_variants)

    def create(self, request, *args, **kwargs):
        pictures_data = request.data.pop("variant_pictures", None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        variant = Variant.objects.get(id=serializer.data.get('id'))

        if pictures_data:
            for picture_file in pictures_data:
                picture_name = picture_file.name
                picture_extension = picture_name.split(".")[-1]
                picture_content = b64encode(picture_file.read()).decode("utf-8")
                picture = Pictures.objects.create(
                    name=picture_name, extention=picture_extension, content=picture_content
                )
                variant.variant_pictures.add(picture.id)
                variant.save()
        return Response(VariantSerializers(variant).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        pictures_data = request.data.getlist("variant_pictures")
        mutable_data = request.data.copy()
        if "variant_pictures" in mutable_data:
            mutable_data.pop("variant_pictures")
        serializer = self.get_serializer(instance, data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        variant = self.get_object()

        for item in pictures_data:
            if isinstance(item, InMemoryUploadedFile):
                picture_file = item
                picture_name = picture_file.name
                picture_extension = picture_name.split(".")[-1]
                picture_content = base64.b64encode(picture_file.read()).decode("utf-8")
                picture = Pictures.objects.create(
                    name=picture_name, extention=picture_extension, content=picture_content
                )
                variant.variant_pictures.add(picture.id)
            else:
                variant.variant_pictures.add(int(item))

        variant.save()

        return Response(VariantSerializers(variant).data, status=status.HTTP_200_OK)





