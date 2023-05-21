import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import (
    SIGNUP_QUERY,
    LOGIN_MUTATION,
    GET_USER_QUERY,
    CREATE_POST_MUTATION,
    CREATE_COMMENT_MUTATION
)
import logging

class TestCreateComment(GraphQLTestCase):
    def setUp(self):
        self.registrationResponse = self.query(
            SIGNUP_QUERY,
            variables = {
                "email": "testUser1@test.com",
                "username": "testUser1",
                "password": "Complexpassword1"
            }
        )

        self.loginResponse = self.query(
            LOGIN_MUTATION,
            variables = {
                "email": "testUser1@test.com",
                "password": "Complexpassword1"
            }
        )
        self.loginResponse = json.loads(self.loginResponse.content)
        self.token = self.loginResponse['data']['tokenAuth']['token']

        self.getUserResponse = self.query(
            GET_USER_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token}
        )
        self.getUserResponse = json.loads(self.getUserResponse.content)

        self.createPostResponse = self.query(
            CREATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "title": "test post title",
                "content": "test post content",
            }
        )
        self.createPostResponse = json.loads(self.createPostResponse.content)
    
    def test_can_create_one_comment(self):
        createCommentResponse1 = self.query(
            CREATE_COMMENT_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "post": self.createPostResponse['data']['createPost']['post']['id'],
                "content": "test post1 comment1 content",
            }
        )
        self.assertEqual(createCommentResponse1.status_code, 200)
        self.assertResponseNoErrors(createCommentResponse1)
        createCommentResponse1 = json.loads(createCommentResponse1.content)
        assert len(createCommentResponse1['data']['createComment']['comment']) == 3

    def test_can_create_multiple_comments(self):
        createCommentResponse1 = self.query(
            CREATE_COMMENT_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "post": self.createPostResponse['data']['createPost']['post']['id'],
                "content": "test post1 comment1 content",
            }
        )
        self.assertEqual(createCommentResponse1.status_code, 200)
        self.assertResponseNoErrors(createCommentResponse1)
        createCommentResponse1 = json.loads(createCommentResponse1.content)
        assert len(createCommentResponse1['data']['createComment']['comment']) == 3

        createCommentResponse2 = self.query(
            CREATE_COMMENT_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "post": self.createPostResponse['data']['createPost']['post']['id'],
                "content": "test post1 comment2 content",
            }
        )
        self.assertEqual(createCommentResponse2.status_code, 200)
        self.assertResponseNoErrors(createCommentResponse2)
        createCommentResponse2 = json.loads(createCommentResponse2.content)
        assert len(createCommentResponse2['data']['createComment']['comment']) == 3

    def test_cant_create_comment_without_token(self):
        logging.disable(logging.ERROR)
        createCommentResponse1 = self.query(
            CREATE_COMMENT_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT "},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "post": self.createPostResponse['data']['createPost']['post']['id'],
                "content": "test post1 comment1 content",
            }
        )

        self.assertEqual(createCommentResponse1.status_code, 200)
        content = json.loads(createCommentResponse1.content)
        assert content['errors'][0]['message'] == "Authentication credentials were not provided"
    
    def test_cant_create_comment_nonexisting_postId(self):
        logging.disable(logging.ERROR)
        createCommentResponse1 = self.query(
            CREATE_COMMENT_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "post": '9999',
                "content": "test post1 comment1 content",
            }
        )

        self.assertEqual(createCommentResponse1.status_code, 200)
        content = json.loads(createCommentResponse1.content)
        assert "a foreign key constraint fails" in content['errors'][0]['message']