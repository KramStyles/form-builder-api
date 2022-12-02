from django.urls import path, include
from rest_framework import routers

from .api import UserViewSet

router = routers.SimpleRouter()
router.register('auth', UserViewSet, basename='user-viewset')

urlpatterns = [path('', include(router.urls))]
