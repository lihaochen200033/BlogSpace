import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import (
    SIGNUP_QUERY,
    LOGIN_MUTATION,
    GET_USER_QUERY,
    CREATE_POST_MUTATION,
    CREATE_COMMENT_MUTATION,
    GET_COMMENTS_QUERY
)
import logging

class TestGetComments(GraphQLTestCase):
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

        self.createCommentResponse1 = self.query(
            CREATE_COMMENT_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "post": self.createPostResponse['data']['createPost']['post']['id'],
                "content": "test post1 comment1 content",
            }
        )
        self.createCommentResponse1 = json.loads(self.createCommentResponse1.content)

        self.createCommentResponse2 = self.query(
            CREATE_COMMENT_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + self.token},
            variables = {
                "author": self.getUserResponse['data']['userDetails']['id'],
                "post": self.createPostResponse['data']['createPost']['post']['id'],
                "content": "test post1 comment2 content",
            }
        )
        self.createCommentResponse2 = json.loads(self.createCommentResponse2.content)
    
    def test_can_get_comments_from_one_user(self):
        getCommentsResponse = self.query(
            GET_COMMENTS_QUERY,
            variables = {"postId": self.createPostResponse['data']['createPost']['post']['id']}
        )
        self.assertEqual(getCommentsResponse.status_code, 200)
        self.assertResponseNoErrors(getCommentsResponse)
        getCommentsResponse = json.loads(getCommentsResponse.content)
        assert len(getCommentsResponse['data']['commentByPostId']) == 2
        assert len(getCommentsResponse['data']['commentByPostId'][0]) == 3
        assert getCommentsResponse['data']['commentByPostId'][0]['content'] \
                == "test post1 comment2 content"
        assert getCommentsResponse['data']['commentByPostId'][1]['content'] \
                == "test post1 comment1 content"

    def test_can_get_comments_from_different_users(self):
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

        createCommentResponse1 = self.query(
            CREATE_COMMENT_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + token},
            variables = {
                "author": getUserResponse['data']['userDetails']['id'],
                "post": self.createPostResponse['data']['createPost']['post']['id'],
                "content": "test post1 comment1 user 2 content",
            }
        )
        createCommentResponse1 = json.loads(createCommentResponse1.content)

        createCommentResponse2 = self.query(
            CREATE_COMMENT_MUTATION,
            headers = {'HTTP_AUTHORIZATION': "JWT " + token},
            variables = {
                "author": getUserResponse['data']['userDetails']['id'],
                "post": self.createPostResponse['data']['createPost']['post']['id'],
                "content": "test post1 comment2 user 2 content",
            }
        )
        createCommentResponse2 = json.loads(createCommentResponse2.content)

        getCommentsResponse = self.query(
            GET_COMMENTS_QUERY,
            variables = {"postId": self.createPostResponse['data']['createPost']['post']['id']}
        )
        self.assertEqual(getCommentsResponse.status_code, 200)
        self.assertResponseNoErrors(getCommentsResponse)
        getCommentsResponse = json.loads(getCommentsResponse.content)
        assert len(getCommentsResponse['data']['commentByPostId']) == 4
        assert getCommentsResponse['data']['commentByPostId'][0]['content'] \
                == "test post1 comment2 user 2 content"
        assert getCommentsResponse['data']['commentByPostId'][1]['content'] \
                == "test post1 comment1 user 2 content"
        assert getCommentsResponse['data']['commentByPostId'][2]['content'] \
                == "test post1 comment2 content"
        assert getCommentsResponse['data']['commentByPostId'][3]['content'] \
                == "test post1 comment1 content"
        
    def test_cant_get_post_non_existing_postId(self):
        logging.disable(logging.ERROR)
        getCommentsResponse = self.query(
            GET_COMMENTS_QUERY,
            variables = {"postId": '9999'}
        )
        self.assertEqual(getCommentsResponse.status_code, 200)
        getCommentsResponse = json.loads(getCommentsResponse.content)
        assert getCommentsResponse['data']['commentByPostId'] == []
