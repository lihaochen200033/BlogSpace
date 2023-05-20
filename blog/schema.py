import graphene
from graphene_django import DjangoObjectType
from .models import Post, Comment

#******************************* Blog Queries **************************************#

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "author", "created_on", "updated_on")

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "post", "author", "content", "created_on", "updated_on")

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, post_id=graphene.ID(required=True))
    comment_by_post_id = graphene.List(CommentType, post_id=graphene.ID(required=True))

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_post_by_id(root, info, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return None
    
    def resolve_comment_by_post_id(root, info, post_id):
        try:
            return Comment.objects.filter(post_id=post_id)
        except Comment.DoesNotExist:
            return None


#******************************* Blog Mutations **************************************#

########################################
########### Comment Section ############
########################################

class CreateComment(graphene.Mutation):
    class Arguments:
        post = graphene.ID(required=True)
        author = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, post, author, content=None):
        # check authentication
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        comment = Comment.objects.create(
            post_id = post,
            author_id = author,
            content = content,
        )

        comment.save()
        
        return CreateComment(comment=comment)

class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    comment = graphene.Field(CommentType)
    
    def mutate(self, info, id):
        # check authentication
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        comment = Comment.objects.get(pk=id)

        if comment is not None:
            comment.delete()
        
        comment.id = id
        return DeleteComment(comment=comment)
    
########################################
############# Post Section #############
########################################

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author = graphene.ID(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, title, author, content=None):
        # check authentication
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        post = Post.objects.create(
            title = title,
            author_id = author,
            content = content,
        )

        post.save()
        
        return CreatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, id):
        # check authentication
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        post = Post.objects.get(pk=id)

        if post is not None:
            post.delete()
        
        post.id = id
        return DeletePost(post=post)
    
class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, id, title=None, content=None):
        # check authentication
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        post = Post.objects.get(pk=id)
        post.title = title if title else post.title
        post.content = content if content else post.content

        post.save()
        
        return UpdatePost(post=post)
    
#******************************* Wire up Mutations **************************************#

class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
