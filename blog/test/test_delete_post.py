import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import (
    SIGNUP_QUERY,
    LOGIN_MUTATION,
    GET_USER_QUERY,
    CREATE_POST_MUTATION,
    GET_ALL_POST,
    DELETE_POST_MUTATION
)
import logging

class TestDeletePost(GraphQLTestCase):
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

        self.getAllPostResponse = self.query(
            GET_ALL_POST,
        )
        self.getAllPostResponse = json.loads(self.getAllPostResponse.content)
    
    def test_can_delete_one_post_with_one_user(self):
        deletePostResponse = self.query(
            DELETE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {"id": self.getAllPostResponse['data']['allPosts'][0]['id']}
        )
        self.assertEqual(deletePostResponse.status_code, 200)
        self.assertResponseNoErrors(deletePostResponse)
        deletePostResponse = json.loads(deletePostResponse.content)
        assert len(deletePostResponse['data']['deletePost']) == 1

        getAllPostResponse = self.query(
            GET_ALL_POST,
        )
        self.assertEqual(getAllPostResponse.status_code, 200)
        self.assertResponseNoErrors(getAllPostResponse)
        getAllPostResponse = json.loads(getAllPostResponse.content)
        assert len(getAllPostResponse['data']['allPosts']) == 1
        assert getAllPostResponse['data']['allPosts'][0]['title'] == "test post title 1"

    def test_can_delete_all_posts_with_one_user(self):
        deletePostResponse1 = self.query(
            DELETE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {"id": self.getAllPostResponse['data']['allPosts'][0]['id']}
        )

        deletePostResponse2 = self.query(
            DELETE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {"id": self.getAllPostResponse['data']['allPosts'][1]['id']}
        )

        getAllPostResponse = self.query(
            GET_ALL_POST,
        )
        self.assertEqual(getAllPostResponse.status_code, 200)
        self.assertResponseNoErrors(getAllPostResponse)
        getAllPostResponse = json.loads(getAllPostResponse.content)
        assert getAllPostResponse['data']['allPosts'] == []
    
    def test_can_delete_post_with_multiple_user(self):
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
                "title": "test post title 1 user 2",
                "content": "test post content 1 user 2",
            }
        )
        createPostResponse1 = json.loads(createPostResponse1.content)
        
        createPostResponse2 = self.query(
            CREATE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + token},
            variables = {
                "author": getUserResponse['data']['userDetails']['id'],
                "title": "test post title 2 user 2",
                "content": "test post content 2 user 2",
            }
        )
        createPostResponse2 = json.loads(createPostResponse2.content)

        getAllPostResponse = self.query(
            GET_ALL_POST,
        )
        getAllPostResponse = json.loads(getAllPostResponse.content)

        deletePostResponse1 = self.query(
            DELETE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {"id": getAllPostResponse['data']['allPosts'][2]['id']}
        )

        getAllPostResponse = self.query(
            GET_ALL_POST,
        )
        self.assertEqual(getAllPostResponse.status_code, 200)
        self.assertResponseNoErrors(getAllPostResponse)
        getAllPostResponse = json.loads(getAllPostResponse.content)
        assert len(getAllPostResponse['data']['allPosts']) == 3
        assert getAllPostResponse['data']['allPosts'][0]['title'] \
                == "test post title 2 user 2"
        assert getAllPostResponse['data']['allPosts'][1]['title'] \
                == "test post title 1 user 2"
        assert getAllPostResponse['data']['allPosts'][2]['title'] \
                == "test post title 1"

    def test_cant_delete_post_non_existing_postId(self):
        logging.disable(logging.ERROR)
        deletePostResponse1 = self.query(
            DELETE_POST_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {"id": '9999'}
        )
        self.assertEqual(deletePostResponse1.status_code, 200)
        deletePostResponse1 = json.loads(deletePostResponse1.content)
        assert deletePostResponse1['errors'][0]['message'] == "Post matching query does not exist."

    def test_cant_delete_post_without_token(self):
        logging.disable(logging.ERROR)
        deletePostResponse1 = self.query(
            DELETE_POST_MUTATION,
            variables = {"id": self.getAllPostResponse['data']['allPosts'][0]['id']}
        )
        self.assertEqual(deletePostResponse1.status_code, 200)
        deletePostResponse1 = json.loads(deletePostResponse1.content)
        assert deletePostResponse1['errors'][0]['message'] == "Authentication credentials were not provided"
    