from rest_framework.serializers import ModelSerializer

from apps.pictures.serializers import PicturesSerializers
from apps.products.models import Category, Product, Article, Variant
from apps.users.serializers import MinimalUserSerializers


class VariantSerializersMinimal(ModelSerializer):
    variant_pictures = PicturesSerializers(many=True)

    class Meta:
        model = Variant
        fields = ['id', 'color', 'size', 'type', 'price', 'is_active', 'is_sold', "variant_pictures"]


class MinimalCategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
    

class ProductSerializersMinimal(ModelSerializer):
    category = MinimalCategorySerializers(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'is_active', 'category']


class MinimalListArticleSerializers(ModelSerializer):
    variants = VariantSerializersMinimal(many=True)
    product = ProductSerializersMinimal(read_only=True)
    article_pictures = PicturesSerializers(many=True)

    class Meta:
        model = Article
        fields = ['id', 'name', 'price', 'is_active', 'is_sold', 'product', 'description', 'variants', "article_pictures"]


class MinimalRetriveArticleSerializers(ModelSerializer):
    variants = VariantSerializersMinimal(many=True)
    product = ProductSerializersMinimal(read_only=True)
    article_pictures = PicturesSerializers(many=True)

    class Meta:
        model = Article
        fields = ['id', 'name', 'price', 'is_active', 'is_sold', 'product', 'variants', "article_pictures"]


class ArticleSerializersMinimal(ModelSerializer):
    variants = VariantSerializersMinimal(many=True)

    class Meta:
        model = Article
        fields = ['id', 'name', 'price', 'is_active', 'is_sold', 'variants']


class MinimalProductSerializers(ModelSerializer):
    articles = ArticleSerializersMinimal(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'is_active', 'articles']


class MinimalListProductSerializers(ModelSerializer):
    category = MinimalCategorySerializers(read_only=True)
    articles = ArticleSerializersMinimal(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'is_active', 'articles', 'category']


class MinimalListCategorySerializers(ModelSerializer):
    products = MinimalProductSerializers(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']


class ProductSerializers(ModelSerializer):
    creator = MinimalUserSerializers(read_only=True)
    last_author = MinimalUserSerializers(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['category'] = MinimalCategorySerializers(read_only=True)

        return super(ProductSerializers, self).to_representation(instance)


class CategorySerializers(ModelSerializer):
    creator = MinimalUserSerializers(read_only=True)
    last_author = MinimalUserSerializers(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializers(ModelSerializer):
    creator = MinimalUserSerializers(read_only=True)
    last_author = MinimalUserSerializers(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializersMinimal(read_only=True)
        self.fields['article_pictures'] = PicturesSerializers(many=True, read_only=True)

        return super(ArticleSerializers, self).to_representation(instance)


class MinimalArticleSerializers(ModelSerializer):
    product = ProductSerializersMinimal(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'name', 'product']


class VariantSerializers(ModelSerializer):
    creator = MinimalUserSerializers(read_only=True)
    last_author = MinimalUserSerializers(read_only=True)

    class Meta:
        model = Variant
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['article'] = MinimalArticleSerializers(read_only=True)

        return super(VariantSerializers, self).to_representation(instance)


class MinimalListVariantSerializers(ModelSerializer):
    article = MinimalArticleSerializers(read_only=True)

    class Meta:
        model = Variant
        fields = ['id', 'article', 'color', 'size', 'type', 'price', 'is_active', 'is_sold']




