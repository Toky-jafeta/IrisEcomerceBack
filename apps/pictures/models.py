from django.db import models

from common.models import BaseModel


class Pictures(BaseModel):
    name = models.CharField(max_length=50)
    extention = models.CharField(max_length=5)
    content = models.TextField()
