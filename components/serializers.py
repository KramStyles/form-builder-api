from rest_framework import serializers

from .models import Forms, Elements, Details
from authentication.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_type']


class ElementSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Elements
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context.get('user')
        return super().create(validated_data)


class FormsSerializer(ElementSerializer):
    class Meta(ElementSerializer.Meta):
        model = Forms

    def create(self, validated_data):
        validated_data['author'] = self.context.get('user')
        return super().create(validated_data)


class DetailSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)

    class Meta:
        model = Details
        fields = '__all__'

    def validate(self, attrs):
        user = self.context.get('user')
        # We check if the form has been filled by the user to prevent him from filling the same form again
        form = attrs.get('form')
        if Details.objects.filter(user=user, form=form):
            raise serializers.ValidationError({'error': 'You have filled this form. Edit it instead!'})

        if form.fields and (len(form.fields) != len(attrs.get('values'))):
            raise serializers.ValidationError({'error': "Values don't match. Something is wrong"})

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        try:
            Details.objects.create(**validated_data)
        except (TypeError, ValueError) as err:
            raise serializers.ValidationError({'error': str(err)})
        validated_data['message'] = 'Form Saved!'
        return validated_data


class DetailEditSerializer(DetailSerializer):
    form_data = serializers.SerializerMethodField()

    def get_form_data(self, obj):
        data = {
            'name': obj.form.name,
            'desc': obj.form.description
        }
        return data

    def validate(self, attrs):
        # This double checks to ensure only the owner can edit the form
        user = self.context.get('request').user
        owner = self.instance.user
        if user != owner:
            raise serializers.ValidationError({'error': "You don't have the permission to edit this form"})
        return attrs
