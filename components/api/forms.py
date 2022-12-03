from rest_framework import generics, response, status, permissions

from authentication.permissions import FormBuilderPermissions


from components.serializers import Forms, FormsSerializer


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


class FetchFormsListAPIView(generics.ListAPIView):
    """This endpoint displays the published forms to be filled by all users"""
    queryset = Forms.objects.exclude(fields__isnull=True)
    serializer_class = FormsSerializer
