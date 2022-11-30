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
