from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from apps.clients.models import Client
from apps.clients.serializers import ClientSerializers


class ClientViewset(ModelViewSet):
    serializer_class = ClientSerializers
    queryset = Client.objects.all()
