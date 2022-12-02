from django.urls import path

from .api import (FormsListCreateApiView, FormsEditApiView, ElementListCreateAPIView, ElementEditAPIView,
                  FetchFormsListAPIView, DetailListCreateAPIView, DetailEditAPIView)


urlpatterns = [
    path('forms/', FormsListCreateApiView.as_view(), name='form-list'),
    path('elements/', ElementListCreateAPIView.as_view(), name='element-list'),
    path('details/', DetailListCreateAPIView.as_view(), name='details-list'),

    path('forms/<int:pk>/', FormsEditApiView.as_view(), name='forms-edit'),
    path('elements/<int:pk>/', ElementEditAPIView.as_view(), name='element-edit'),
    path('details/<int:pk>/', DetailEditAPIView.as_view(), name='detail-edit'),

    path('forms/fetch/', FetchFormsListAPIView.as_view(), name='fetch-forms'),
]
