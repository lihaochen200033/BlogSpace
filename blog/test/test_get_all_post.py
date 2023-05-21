import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import (
    SIGNUP_QUERY,
    LOGIN_MUTATION,
    GET_USER_QUERY,
    CREATE_POST_MUTATION,
    GET_ALL_POST
)
import logging

class TestGetAllPost(GraphQLTestCase):
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

        self.createPostResponse1 = self.query(
            CREATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "title": "test post title 1",
                "content": "test post content 1",
            }
        )
        self.createPostResponse1 = json.loads(self.createPostResponse1.content)

        self.createPostResponse2 = self.query(
            CREATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "title": "test post title 2",
                "content": "test post content 2",
            }
        )
        self.createPostResponse2 = json.loads(self.createPostResponse2.content)

    def test_can_get_all_post_from_one_user(self):
        getAllPostResponse = self.query(
            GET_ALL_POST,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
        )
        self.assertEqual(getAllPostResponse.status_code, 200)
        self.assertResponseNoErrors(getAllPostResponse)
        getAllPostResponse = json.loads(getAllPostResponse.content)
        assert len(getAllPostResponse['data']['allPosts']) == 2

    def test_can_get_all_post_from_different_user(self):
        registrationResponse = self.query(
            SIGNUP_QUERY,
            variables = {
                "email": "testUser2@test.com",
                "username": "testUser2",
                "password": "Complexpassword2"
            }
        )

        loginResponse = self.query(
            LOGIN_MUTATION,
            variables = {
                "email": "testUser2@test.com",
                "password": "Complexpassword2"
            }
        )
        loginResponse = json.loads(loginResponse.content)
        token = loginResponse['data']['tokenAuth']['token']
        getUserResponse = self.query(
            GET_USER_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT " + token}
        )
        getUserResponse = json.loads(getUserResponse.content)

        createPostResponse1 = self.query(
            CREATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + token},
            variables = {
                "author": getUserResponse['data']['userDetails']['id'],
                "title": "test post title 3",
                "content": "test post content 3",
            }
        )
        createPostResponse1 = json.loads(createPostResponse1.content)

        getAllPostResponse = self.query(
            GET_ALL_POST,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
        )
        self.assertEqual(getAllPostResponse.status_code, 200)
        self.assertResponseNoErrors(getAllPostResponse)
        getAllPostResponse = json.loads(getAllPostResponse.content)
        assert len(getAllPostResponse['data']['allPosts']) == 3
        assert getAllPostResponse['data']['allPosts'][0]['title'] \
                == "test post title 3"
        assert getAllPostResponse['data']['allPosts'][1]['title'] \
                == "test post title 2"
        assert getAllPostResponse['data']['allPosts'][2]['title'] \
                == "test post title 1"
