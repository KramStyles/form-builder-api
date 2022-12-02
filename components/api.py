from rest_framework import generics, response, status, permissions

from authentication.permissions import AdminPermissions, FormBuilderPermissions
from .serializers import *


class FormsListCreateApiView(generics.ListCreateAPIView):
    """This endpoint creates and lists forms"""
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer
    permission_classes = [permissions.IsAuthenticated, FormBuilderPermissions]

    def get_permissions(self):
        if self.request.method == 'GET':
            # This allows authenticated users to view the forms but only form-builders can create forms
            return [permissions.IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        user = {'user': request.user}
        serializer = self.serializer_class(data=request.data, context=user)
        serializer.is_valid(True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class FormsEditApiView(generics.RetrieveUpdateDestroyAPIView):
    """This endpoint is used to update and delete created forms by either the admin or the owner of the former"""
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer
    permission_classes = [permissions.IsAuthenticated, FormBuilderPermissions]


class ElementListCreateAPIView(FormsListCreateApiView):
    """This endpoint creates and list elements. Elements are accessible to everyone but can
        only be created by the admin
    """

    queryset = Elements.objects.all()
    serializer_class = ElementSerializer
    permission_classes = [permissions.IsAuthenticated, AdminPermissions]

    def create(self, request, *args, **kwargs):
        user = {'user': request.user}
        serializer = self.serializer_class(data=request.data, context=user)
        serializer.is_valid(True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
