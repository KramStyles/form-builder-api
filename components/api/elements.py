from rest_framework import response, status, permissions

from authentication.permissions import AdminPermissions


from components.serializers import Elements, ElementSerializer
from .forms import FormsListCreateApiView, FormsEditApiView


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


class ElementEditAPIView(FormsEditApiView):
    """This endpoint is used to update and delete created elements by admins"""
    queryset = Elements.objects.all()
    serializer_class = ElementSerializer

