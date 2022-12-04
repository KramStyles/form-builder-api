from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'refresh', 'access']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        errors = {}

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                errors['detail'] = 'Invalid authentication details'
        except User.DoesNotExist:
            errors['username'] = "User not found"

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        tokens = RefreshToken.for_user(user)
        validated_data['refresh'] = str(tokens)
        validated_data['access'] = str(tokens.access_token)
        return validated_data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        errors = {}

        if User.objects.filter(username=username):
            errors['username'] = 'User exists with this username'
        if User.objects.filter(email=email):
            errors['email'] = 'User exists with this email address'
        if len(password) < 4:
            errors['password'] = 'Your password is too short'

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        try:
            password = validated_data.get('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
        except (TypeError, AttributeError) as err:
            raise serializers.ValidationError({'error': str(err)})

        return user
