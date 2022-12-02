from rest_framework import generics, response, status

from components.serializers import Details, DetailSerializer


class DetailListCreateAPIView(generics.ListCreateAPIView):
    # This endpoint gets the forms filled by a user. It also lets a user fill a form the first time
    serializer_class = DetailSerializer

    def get_queryset(self):
        details = Details.objects.filter(user=self.request.user)
        return details

    def create(self, request, *args, **kwargs):
        user = {'user': request.user}
        serializer = self.serializer_class(data=request.data, context=user)
        serializer.is_valid(True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)