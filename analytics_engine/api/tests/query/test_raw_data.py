from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from django.core.urlresolvers import reverse
from rest_framework import status
from ae_reflex.models import User, Project


class RawDataQueryTestCase(TestCase):

    def setUp(self):
        self.client = client = APIClient()
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get('/')
        register_url = reverse('register')
        data = {"username": "userA", "password": "123456"}
        client.post(register_url, data)
        self.user = User.objects.get(username=data['username'])
        client.force_authenticate(self.user)

        create_project_url = reverse('create_project')
        data = {"name": "Page Views"}
        response = client.post(create_project_url, data)
        self.external_id = external_id = response.data['external_id']
        self.project = Project.objects.get(external_id=external_id)

    def test_get_events(self):
        raw_data_url = reverse('raw_query', kwargs={"external_id": self.external_id})
        data = {}
        response = self.client.post(raw_data_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('events', response.data)
