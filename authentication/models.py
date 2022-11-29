from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser, BaseModel):
    class USERTYPE(models.TextChoices):
        NORMAL = 'normal', 'Normal'
        BUILDER = 'form-builder', 'Form Builder'
        ADMIN = 'admin', 'Admin'

    user_type = models.CharField(max_length=25, default=USERTYPE.NORMAL, choices=USERTYPE.choices)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
