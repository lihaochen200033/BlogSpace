import random

from django.db import transaction
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from blog.models import Post, Comment
from blog.factories import (
    PostFactory,
    CommentFactory
)

from users.factories import (
    UserFactory,
)

NUM_USERS = 5
NUM_POSTS = 100
COMMENTS_PER_THREAD = [1, 2, 3]

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Post, Comment]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        users = []
        for _ in range(NUM_USERS):
            user = UserFactory()
            users.append(user)

        # Create Posts
        for _ in range(NUM_POSTS):
            author = random.choice(users)
            post = PostFactory(author = author)
            COMMENT_CUR_POST = random.choice(COMMENTS_PER_THREAD)
            # Create comments for the post
            for _ in range(COMMENT_CUR_POST):
                author = random.choice(users)
                CommentFactory(
                    author=author,
                    post=post,
                )
