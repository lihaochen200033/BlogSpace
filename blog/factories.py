import factory
from factory.django import DjangoModelFactory
from .models import Post, Comment
from users.factories import UserFactory

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True
    )
    content = factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True
    )

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    content = factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True
    )