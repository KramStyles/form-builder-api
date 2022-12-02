import json

from django.shortcuts import reverse
from rest_framework.test import APITestCase

from .factories import *


class TestLogin(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.builder = FormBuilderFactory()
        self.admin = AdminFactory()
        self.url = reverse('user-viewset-login')
        self.data = {
            'username': 'michael',
            'password': 'pass'
        }

    def test_to_login_accurately(self):
        response = self.client.post(self.url, data=self.data)
        content = json.loads(response.content)

        self.assertTrue('michael', content.get('username'))
        self.assertIn('refresh', content)
        self.assertIn('access', content)
        self.assertTrue(response.status_code, 200)

    def test_to_login_with_invalid_user(self):
        self.data['username'] = 'mark'
        response = self.client.post(self.url, data=self.data)
        content = json.loads(response.content)

        self.assertTrue('User not found', content.get('username'))
        self.assertIn('username', content)
        self.assertTrue(response.status_code, 400)

    def test_to_login_with_wrong_credentials(self):
        self.data['password'] = 'mark'
        response = self.client.post(self.url, data=self.data)
        content = json.loads(response.content)

        self.assertIn('Invalid', content.get('detail')[0])
        self.assertIn('detail', content)
        self.assertTrue(response.status_code, 400)


class TestRegister(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.builder = FormBuilderFactory()
        self.admin = AdminFactory()
        self.url = reverse('user-viewset-register')
        self.data = {
            'username': 'timizuo',
            'email': 'timizuo@formbuilder.com',
            'password': 'pass'
        }

    def test_to_register_successfully(self):
        response = self.client.post(self.url, data=self.data)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertIn('message', content)
        self.assertEqual('User registered', content.get('message'))

    def test_to_register_with_existing_contact(self):
        self.data['username'] = 'admin'
        response = self.client.post(self.url, data=self.data)
        content = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertIn('username', content)
        self.assertIn('User exists', content.get('username')[0])
