from django.db import models

from authentication.models import User


class Forms(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    fields = models.JSONField(null=True)

    def __str__(self):
        return self.name


class Elements(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    values = models.JSONField(null=True)
