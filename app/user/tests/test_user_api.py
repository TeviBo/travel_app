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


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": fake.email(),
            "password": fake.password(),
            "full_name": f"{fake.first_name()} {fake.last_name()}"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)
