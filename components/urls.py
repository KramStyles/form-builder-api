from django.urls import path

from .api import FormsListCreateApiView


urlpatterns = [
    path('forms/', FormsListCreateApiView.as_view(), name='form-list-create')
]
