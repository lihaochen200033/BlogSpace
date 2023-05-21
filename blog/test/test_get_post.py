import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import (
    SIGNUP_QUERY,
    LOGIN_MUTATION,
    GET_USER_QUERY,
    CREATE_POST_MUTATION,
    GET_POST_QUERY
)
import logging

class TestGetPost(GraphQLTestCase):
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
    
    def test_can_get_post(self):
        getPostResponse = self.query(
            GET_POST_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {"postId": self.createPostResponse['data']['createPost']['post']['id']}
        )
        self.assertEqual(getPostResponse.status_code, 200)
        self.assertResponseNoErrors(getPostResponse)
        getPostResponse = json.loads(getPostResponse.content)
        assert len(getPostResponse['data']['postById']) == 6
        assert getPostResponse['data']['postById']['title'] == "test post title"
        assert getPostResponse['data']['postById']['content'] == "test post content"
        assert getPostResponse['data']['postById']['author']['id'] \
                == self.getUserResponse['data']['userDetails']['id']

    def test_cant_get_post_non_existing_postId(self):
        logging.disable(logging.ERROR)
        getPostResponse = self.query(
            GET_POST_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {"postId": '9999'}
        )
        self.assertEqual(getPostResponse.status_code, 200)
        getPostResponse = json.loads(getPostResponse.content)
        assert getPostResponse['data']['postById'] == None
