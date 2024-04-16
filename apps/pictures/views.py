from rest_framework.viewsets import ModelViewSet

from apps.pictures.models import Pictures
from apps.pictures.serializers import PicturesSerializers


class PicturesViewset(ModelViewSet):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializers
