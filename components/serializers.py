from rest_framework import serializers

from .models import Forms


class FormsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = Forms
        fields = '__all__'
