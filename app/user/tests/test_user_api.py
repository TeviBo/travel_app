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

# FAKEr
from faker import Faker

# CONSTANTS
CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:login")
PROFILE_URL = reverse("user:profile")
FAKE = Faker()

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
            "email": FAKE.email(),
            "password": "Ab123456",
            "full_name": f"{FAKE.first_name()} {FAKE.last_name()}",
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
            "email": FAKE.email(),
            "password": "Ab123456",
            "full_name": f"{FAKE.first_name()} {FAKE.last_name()}",
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_short_password(self):
        """
        Test creating an user with short password throws an error.
        """
        payload = {
            "email": FAKE.email(),
            "password": "Ab123",
            "full_name": f"{FAKE.first_name()} {FAKE.last_name()}",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)

    def test_create_new_user_token(self):
        """Test for token generation."""
        user_details = {
            "email": FAKE.email(),
            "password": "Ab123456",
        }

        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_create_token_bad_credentials_error(self):
        """Test generates token throws an error if bad credentials"""

        create_user(email="test@example.com", password="goodpass")

        # Bad email
        payload = {
            "email": "bademail@gmail.com",
            "password": "goodpass",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Bad password
        payload = {
            "email": "test@example.com",
            "password": FAKE.password(),
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_email_not_found_error(self):
        """Test generates token throws an error if email not found."""

        payload = {
            "email": FAKE.email(),
            "passwod": FAKE.password(),
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_blank_password_error(self):
        """Test generates token throws an error if password is blank."""
        payload = {
            "email": "test@email.com",
            "password": "",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)


class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email=FAKE.email(),
            password="Ab123456",
            full_name=f"{FAKE.first_name()} {FAKE.last_name()}",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""

        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, {"full_name": self.user.full_name, "email": self.user.email}
        )

    def test_post_profile_not_allowed(self):
        """Test that POST is not allowed on the profile url for unauthorized users."""

        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_profile(self):
        """Test updating the profile for authenticated user."""

        payload = {"full_name": "New Name", "password": "NewPassword123"}

        res = self.client.patch(PROFILE_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.full_name, payload["full_name"])
        self.assertTrue(self.user.check_password(payload["password"]))
