import json

from django.shortcuts import reverse
from rest_framework.test import APITestCase

from components.factories import FormsFactory
from authentication.factories import UserFactory, FormBuilderFactory


class TestForms(APITestCase):
    def setUp(self) -> None:
        self.forms = FormsFactory()
        self.user = UserFactory()
        self.builder = FormBuilderFactory()
        self.builder2 = FormBuilderFactory(username="builder2")
        self.data = {
            "name": "Know your customer",
            "description": "This is a KYC form"
        }

    def test_to_ensure_user_is_logged_in(self):
        response = self.client.get(reverse('form-list'))
        content = json.loads(response.content)

        self.assertTrue(response.status_code, 401)
        self.assertIn('Authentication credentials', content.get('detail'))

    def test_to_get_existing_forms(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('form-list'))
        content = json.loads(response.content)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(type(content), list)

    def test_to_create_form_without_permission(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('form-list'), data=self.data)
        content = json.loads(response.content)

        self.assertTrue(response.status_code, 403)
        self.assertEqual('You do not have permission to perform this action.', content.get('detail'))

    def test_to_create_and_get_form_successfully(self):
        with self.subTest('Test to create form successfully'):
            self.client.force_authenticate(self.builder)
            response = self.client.post(reverse('form-list'), data=self.data)
            content = json.loads(response.content)

            self.assertTrue(response.status_code, 201)
            self.assertEqual(self.data.get('name'), content.get('name'))
            self.assertEqual(self.builder.username, content.get('author').get('username'))

        with self.subTest('Test to ensure a form has been created'):
            response = self.client.get(reverse('form-list'))
            content = json.loads(response.content)

            self.assertTrue(response.status_code, 200)
            self.assertEqual(len(content), 2)

        with self.subTest('Test to ensure only creator can edit form'):
            self.client.force_authenticate(self.builder2)
            response = self.client.get(reverse('form-edit', args=[self.forms.pk]))
            content = json.loads(response.content)

            self.assertEqual(response.status_code, 403)
            self.assertTrue('You do not have permission to perform this action.', content.get('detail'))
