import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import SIGNUP_QUERY, GET_USER_QUERY
import logging

class TestGetUser(GraphQLTestCase):
    def setUp(self):
        self.registrationResponse = self.query(
            SIGNUP_QUERY,
            variables = {
                "email": "testUser1@test.com",
                "username": "testUser1",
                "password": "Complexpassword1"
            }
        )
    
    def test_can_get_user(self):
        registrationResponse = json.loads(self.registrationResponse.content)

        getUserResponse = self.query(
            GET_USER_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT " + registrationResponse['data']['register']['token']}
        )

        self.assertEqual(getUserResponse.status_code, 200)
        content = json.loads(getUserResponse.content)
        self.assertResponseNoErrors(getUserResponse)
        assert len(content['data']['userDetails']) == 2
        assert content['data']['userDetails']['username'] == "testUser1"

    def test_cant_get_user_without_token(self):
        logging.disable(logging.ERROR)
        getUserResponse = self.query(
            GET_USER_QUERY,
            headers = {'HTTP_AUTHORIZATION': "JWT "}
        )
        self.assertEqual(getUserResponse.status_code, 200)
        content = json.loads(getUserResponse.content)
        assert content['errors'][0]['message'] == "Authentication credentials were not provided"
