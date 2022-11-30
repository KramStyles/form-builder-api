from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
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
            if user.check_password(password):
                if not user.is_verified:
                    tokens = RefreshToken.for_user(user)
                    attrs['refresh'] = str(tokens)
                    attrs['access'] = str(tokens.access_token)
                else:
                    errors['inactive'] = 'Please verify your account'
            else:
                errors['detail'] = 'Invalid authentication details'
        except User.DoesNotExist:
            errors['username'] = "User not found"

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def save(self, **kwargs):
        return self.data


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

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        try:
            password = validated_data.get('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
        except:
            raise serializers.ValidationError('problem')

        return user
