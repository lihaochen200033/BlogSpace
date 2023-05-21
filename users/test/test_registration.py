import json
from graphene_django.utils.testing import GraphQLTestCase
from core.tests.test_query import SIGNUP_QUERY

class TestRegistration(GraphQLTestCase):
    def test_can_register_user(self):
        response = self.query(
            SIGNUP_QUERY,
            variables = {
                "email": "testUser1@test.com",
                "username": "testUser1",
                "password": "Complexpassword1"
            }
        )

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        assert len(content['data']['register']) == 3
        assert content['data']['register']['success'] == True

    def test_cant_register_user_with_short_password(self):
        response = self.query(
            SIGNUP_QUERY,
            variables = {
                "email": "testUser1@test.com",
                "username": "testUser1",
                "password": "short"
            }
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        assert len(content['data']['register']) == 3
        assert content['data']['register']['success'] == False

    def test_cant_register_user_with_invalid_email(self):
        response = self.query(
            SIGNUP_QUERY,
            variables = {
                "email": "testUser1",
                "username": "testUser1",
                "password": "short"
            }
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        assert len(content['data']['register']) == 3
        assert content['data']['register']['success'] == False