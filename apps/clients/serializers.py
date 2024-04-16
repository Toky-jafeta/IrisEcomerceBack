from rest_framework.serializers import ModelSerializer

from apps.clients.models import Client


class ClientSerializers(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'