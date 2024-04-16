from django.db import models


class Client(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, default=None)
    email = models.EmailField(null=True, default=None)
    address = models.TextField(default=None)
    localization = models.CharField(max_length=255, default=None)

