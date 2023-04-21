"""
Tests for the user API.
"""
# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# DRF
from rest_framework import status
from rest_framework.test import APIClient

# Faker
from faker import Faker

CREATE_USER_URL = reverse("user:create")
fake = Faker()

# Reusable functions


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


# Tests
class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": fake.email(),
            "password": "Ab123456",
            "full_name": f"{fake.first_name()} {fake.last_name()}",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_create_user_with_existing_email(self):
        """
        Test creating a user with an existing email throws an error."""
        payload = {
            "email": fake.email(),
            "password": "Ab123456",
            "full_name": f"{fake.first_name()} {fake.last_name()}",
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_short_password(self):
        """
        Test creating an user with short password throws an error.
        """
        payload = {
            'email': fake.email(),
            'password': 'Ab123',
            'full_name': f'{fake.first_name()} {fake.last_name()}',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)
