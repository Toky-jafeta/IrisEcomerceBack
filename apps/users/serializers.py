from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", )


class MinimalUserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']