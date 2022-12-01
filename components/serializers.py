from rest_framework import serializers

from .models import Forms
from authentication.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_type']


class FormsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Forms
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context.get('user')
        try:
            Forms.objects.create(**validated_data)
        except TypeError as err:
            raise serializers.ValidationError({'error': str(err)})

        validated_data['message'] = 'ok'
        return validated_data
