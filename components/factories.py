import factory

from .models import Forms, Elements, Details
from authentication.factories import *


class FormsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Forms

    name = 'Contact form'
    description = 'A basic contact form'
    author = factory.SubFactory(FormBuilderFactory)


class ElementsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Elements

    name = "label"
    author = factory.SubFactory(AdminFactory)


class DetailsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Details

    user = factory.SubFactory(UserFactory)
    form = factory.SubFactory(FormsFactory)
