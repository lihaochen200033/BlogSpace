import factory
from factory.django import DjangoModelFactory

from django.contrib.auth.models import User

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Faker("first_name")
    password = factory.Faker("password")
