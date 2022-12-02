from rest_framework import viewsets, status, response, decorators, permissions

from .models import User
from .serializers import LoginSerializer, RegisterSerializer


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        if self.action == 'register':
            return RegisterSerializer

    @decorators.action(['POST'], False)
    def login(self, request):
        """This endpoint is used to log users in"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(methods=['POST'], detail=False)
    def register(self, request):
        """This endpoint handles the registration of the user"""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return response.Response({'message': 'User registered'}, status=status.HTTP_200_OK)
