from rest_framework.serializers import ModelSerializer

from apps.pictures.models import Pictures


class PicturesSerializers(ModelSerializer):
    class Meta:
        model = Pictures
        fields= '__all__'
