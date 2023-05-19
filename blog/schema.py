import graphene
from graphene_django import DjangoObjectType
from .models import Post, Comment

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("title", "content", "author", "created_on", "updated_on")

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("post", "author", "content", "created_on", "updated_on")

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, post_id=graphene.ID(required=True))

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_post_by_id(root, info, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return None