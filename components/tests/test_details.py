import json

from django.shortcuts import reverse
from rest_framework.test import APITestCase

from components.factories import DetailsFactory, ElementsFactory, FormsFactory
from authentication.factories import UserFactory, AdminFactory


class TestDetails(APITestCase):
    def setUp(self) -> None:
        self.detail = DetailsFactory()
        self.user = UserFactory()
        self.admin = AdminFactory()
        self.form = FormsFactory()

        self.data = {
            "form": self.form.pk
        }

    def test_to_get_existing_details_by_different_users(self):
        with self.subTest('To get a filled form by a user'):
            self.client.force_authenticate(self.user)
            response = self.client.get(reverse('detail-list'))
            content = json.loads(response.content)

            self.assertTrue(response.status_code, 200)
            self.assertTrue(type(content), list)
            self.assertTrue(len(content), 1)

        with self.subTest('Test to ensure a user gets an empty list if he has not filled a form'):
            self.client.force_authenticate(self.admin)
            response = self.client.get(reverse('detail-list'))
            content = json.loads(response.content)

            self.assertTrue(response.status_code, 200)
            self.assertEqual(len(content), 0)

    def test_to_fill_a_form_without_value(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(reverse('detail-list'), data=self.data)
        content = json.loads(response.content)

        self.assertTrue(response.status_code, 400)
        self.assertEqual('This field is required.', content.get('values')[0])

    def test_to_fill_a_form_successfully(self):
        with self.subTest('Test to fill a form'):
            values = [
                {
                    "name": "textbox",
                    "label": "fullname",
                    "value": "Tester Kun"
                },
                {
                    "name": "textarea",
                    "label": "about yourself",
                    "value": "I am a world class developer"
                }
            ]
            self.data["values"] = json.dumps(values)

            self.client.force_authenticate(self.admin)
            response = self.client.post(reverse('detail-list'), data=self.data)
            content = json.loads(response.content)

            self.assertTrue(response.status_code, 201)
            self.assertEqual(self.admin.username, content.get('user').get('username'))
            form_id = content.get('form')

        with self.subTest('Test to edit newly filled form'):
            values = [
                {
                    "name": "textbox",
                    "label": "fullname",
                    "value": "Timizuo"
                },
                {
                    "name": "textarea",
                    "label": "about yourself",
                    "value": "I am a world class developer"
                }
            ]
            self.data["values"] = json.dumps(values)

            self.client.force_authenticate(self.admin)
            response = self.client.patch(reverse('detail-edit', args=(form_id,)), data=self.data)
            content = json.loads(response.content)

            self.assertTrue(response.status_code, 200)
