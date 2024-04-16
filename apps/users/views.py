from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User
from apps.users.serializers import UserSerializers, MinimalUserSerializers


class UserViewset(ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Nom d'utilisateur ou mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)

        token_serializer = TokenObtainPairSerializer(data={"username": username, "password": password})
        token_serializer.is_valid()
        tokens_data = token_serializer.validated_data

        user_serializer = MinimalUserSerializers(user)

        return Response({
            "access_token": tokens_data["access"],
            "refresh_token": tokens_data["refresh"],
            "user": user_serializer.data
        })

    @action(methods=['post'], detail=False)
    def refresh(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        refresh = request.data.get('refresh')


