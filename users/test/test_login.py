import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import SIGNUP_QUERY, LOGIN_MUTATION

class TestLogin(GraphQLTestCase):
    def setUp(self):
        registrationResponse = self.query(
            SIGNUP_QUERY,
            variables = {
                "email": "testUser1@test.com",
                "username": "testUser1",
                "password": "Complexpassword1"
            }
        )
    
    def test_can_login(self):
        response = self.query(
            LOGIN_MUTATION,
            variables = {
                "email": "testUser1@test.com",
                "password": "Complexpassword1"
            }
        )

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        assert len(content['data']['tokenAuth']) == 3
        assert content['data']['tokenAuth']['success'] == True

    def test_cant_login_with_wrong_password(self):
        response = self.query(
            LOGIN_MUTATION,
            variables = {
                "email": "testUser1@test.com",
                "password": "wrongpassword"
            }
        )

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        assert len(content['data']['tokenAuth']) == 3
        assert content['data']['tokenAuth']['success'] == False

    def test_cant_login_with_wrong_email(self):
        response = self.query(
            LOGIN_MUTATION,
            variables = {
                "email": "wrongemail@test.com",
                "password": "Complexpassword1"
            }
        )

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        assert len(content['data']['tokenAuth']) == 3
        assert content['data']['tokenAuth']['success'] == False
