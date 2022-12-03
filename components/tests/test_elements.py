import json

from django.shortcuts import reverse
from rest_framework.test import APITestCase

from components.factories import ElementsFactory
from authentication.factories import UserFactory, AdminFactory


class TestElements(APITestCase):
    def setUp(self) -> None:
        self.element = ElementsFactory()
        self.user = UserFactory()
        self.admin = AdminFactory()
        self.admin2 = AdminFactory(username="admin2")
        self.data = {
            "name": "textarea",
            "label": "This is a textarea"
        }

    def test_to_ensure_user_is_logged_in(self):
        response = self.client.get(reverse('element-list'))
        content = json.loads(response.content)

        self.assertTrue(response.status_code, 401)
        self.assertIn('Authentication credentials', content.get('detail'))

    def test_to_get_existing_elements(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('element-list'))
        content = json.loads(response.content)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(type(content), list)

    def test_to_create_element_without_permission(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('element-list'), data=self.data)
        content = json.loads(response.content)

        self.assertTrue(response.status_code, 403)
        self.assertEqual('You do not have permission to perform this action.', content.get('detail'))

    def test_to_create_and_get_element_successfully(self):
        with self.subTest('Test to create element successfully'):
            self.client.force_authenticate(self.admin2)
            response = self.client.post(reverse('element-list'), data=self.data)
            content = json.loads(response.content)

            self.assertTrue(response.status_code, 201)
            self.assertEqual(self.data.get('name'), content.get('name'))
            self.assertEqual(self.admin2.username, content.get('author').get('username'))

        with self.subTest('Test to ensure an element has been created'):
            response = self.client.get(reverse('element-list'))
            content = json.loads(response.content)

            self.assertTrue(response.status_code, 200)
            self.assertEqual(len(content), 2)

        with self.subTest('Test to ensure only an admin can edit an element'):
            self.client.force_authenticate(self.user)
            response = self.client.get(reverse('element-edit', args=[self.element.pk]))
            content = json.loads(response.content)

            self.assertEqual(response.status_code, 403)
            self.assertTrue('You do not have permission to perform this action.', content.get('detail'))
