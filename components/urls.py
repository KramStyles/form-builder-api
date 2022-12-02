from django.urls import path

from .api import FormsListCreateApiView, FormsEditApiView


urlpatterns = [
    path('forms/', FormsListCreateApiView.as_view(), name='form-list-create'),
    path('forms/<int:pk>/', FormsEditApiView.as_view(), name='forms-edit'),
]
