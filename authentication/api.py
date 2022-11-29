from rest_framework import viewsets, status, response, decorators, permissions

from .models import User
from .serializers import *


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer

    @decorators.action(['POST'], detail=False)
    def login(self, request):
        """This endpoint is used to log users in"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)
