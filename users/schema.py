import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class Query(UserQuery, MeQuery, graphene.ObjectType):
    user_details = graphene.Field(UserType)

    def resolve_user_details(root, info, **kwargs):
        # check authentication
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        return User.objects.get(username=user)


class Mutation(AuthMutation, graphene.ObjectType):
    pass