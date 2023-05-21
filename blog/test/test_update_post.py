import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import (
    SIGNUP_QUERY,
    LOGIN_MUTATION,
    GET_USER_QUERY,
    CREATE_POST_MUTATION,
    GET_POST_QUERY,
    UPDATE_POST_MUTATION,
)
import logging

class TestUpdatePost(GraphQLTestCase):
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

        self.getPostResponse = self.query(
            GET_POST_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {"postId": self.createPostResponse['data']['createPost']['post']['id']}
        )
        self.getPostResponse = json.loads(self.getPostResponse.content)
    
    def test_can_update_post(self):
        updatePostResponse = self.query(
            UPDATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "id": self.getPostResponse['data']['postById']['id'],
                "title": "test post title updated",
                "content": "test post content updated",
            }
        )
        self.assertEqual(updatePostResponse.status_code, 200)
        self.assertResponseNoErrors(updatePostResponse)
        updatePostResponse = json.loads(updatePostResponse.content)
        assert len(updatePostResponse['data']['updatePost']) == 1
        assert updatePostResponse['data']['updatePost']['post']['id'] == self.getPostResponse['data']['postById']['id']
        
        getUpdatedPostResponse = self.query(
            GET_POST_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {"postId": updatePostResponse['data']['updatePost']['post']['id']}
        )
        getUpdatedPostResponse = json.loads(getUpdatedPostResponse.content)

        assert getUpdatedPostResponse['data']['postById']['title'] \
                == "test post title updated"
        assert getUpdatedPostResponse['data']['postById']['content'] \
                == "test post content updated"

    def test_cant_update_post_without_token(self):
        updatePostResponse = self.query(
            UPDATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT "},
            variables = {
                "id": self.getPostResponse['data']['postById']['id'],
                "title": "test post title updated",
                "content": "test post content updated",
            }
        )
        self.assertEqual(updatePostResponse.status_code, 200)
        updatePostResponse = json.loads(updatePostResponse.content)
        assert updatePostResponse['errors'][0]['message'] == "Authentication credentials were not provided"

    def test_cant_update_post_non_existing_postId(self):
        logging.disable(logging.ERROR)
        updatePostResponse = self.query(
            UPDATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "id": '9999',
                "title": "test post title updated",
                "content": "test post content updated",
            }
        )
        self.assertEqual(updatePostResponse.status_code, 200)
        updatePostResponse = json.loads(updatePostResponse.content)
        assert updatePostResponse['errors'][0]['message'] == "Post matching query does not exist."
