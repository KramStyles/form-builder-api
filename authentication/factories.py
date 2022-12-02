import factory

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )

    password = factory.PostGenerationMethodCall('set_password', 'pass')
    username = 'michael'
    user_type = User.USERTYPE.NORMAL


class FormBuilderFactory(UserFactory):
    username = 'tester'
    user_type = User.USERTYPE.BUILDER


class AdminFactory(UserFactory):
    username = 'admin'
    user_type = User.USERTYPE.ADMIN
