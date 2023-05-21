import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import (
    SIGNUP_QUERY,
    LOGIN_MUTATION,
    GET_USER_QUERY,
    CREATE_POST_MUTATION
)
import logging

class TestCreatePost(GraphQLTestCase):
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
    
    def test_can_create_post(self):
        getUserResponse = self.query(
            GET_USER_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token}
        )
        getUserResponse = json.loads(getUserResponse.content)

        createPostResponse = self.query(
            CREATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": getUserResponse['data']['userDetails']['id'],
                "title": "test post title",
                "content": "test post content",
            }
        )

        self.assertEqual(createPostResponse.status_code, 200)
        self.assertResponseNoErrors(createPostResponse)
        createPostResponse = json.loads(createPostResponse.content)
        assert len(createPostResponse['data']['createPost']) == 1

    def test_cant_create_post_without_token(self):
        logging.disable(logging.ERROR)
        getUserResponse = self.query(
            GET_USER_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token}
        )
        getUserResponse = json.loads(getUserResponse.content)

        createPostResponse = self.query(
            CREATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT "},
            variables = {
                "author": getUserResponse['data']['userDetails']['id'],
                "title": "test post title",
                "content": "test post content",
            }
        )

        self.assertEqual(createPostResponse.status_code, 200)
        content = json.loads(createPostResponse.content)
        assert content['errors'][0]['message'] == "Authentication credentials were not provided"
