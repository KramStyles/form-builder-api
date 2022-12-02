from rest_framework import serializers

from .models import Forms, Elements
from authentication.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_type']


class ElementSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Elements
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context.get('user')
        element_name = validated_data.get('name')
        if Elements.objects.filter(name=element_name):
            raise serializers.ValidationError({'error': f'{element_name} has already been created!'})
        try:
            Elements.objects.create(**validated_data)
        except TypeError as err:
            raise serializers.ValidationError({'error': str(err)})

        validated_data['message'] = 'ok'
        return validated_data


class FormsSerializer(ElementSerializer):
    class Meta(ElementSerializer.Meta):
        model = Forms

    def create(self, validated_data):
        validated_data['author'] = self.context.get('user')
        try:
            Forms.objects.create(**validated_data)
        except TypeError as err:
            raise serializers.ValidationError({'error': str(err)})

        validated_data['message'] = 'ok'
        return validated_data
