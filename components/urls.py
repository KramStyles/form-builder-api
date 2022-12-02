from django.urls import path

from .api import (FormsListCreateApiView, FormsEditApiView, ElementListCreateAPIView, ElementEditAPIView)


urlpatterns = [
    path('forms/', FormsListCreateApiView.as_view(), name='form-list'),
    path('elements/', ElementListCreateAPIView.as_view(), name='element-list'),
    path('forms/<int:pk>/', FormsEditApiView.as_view(), name='forms-edit'),
    path('elements/<int:pk>/', ElementEditAPIView.as_view(), name='element-edit'),
]
