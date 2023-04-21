# Imports

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase


# Reusable functions:
def sample_user(email="email@sample.com", password="test123"):
    """
    Creates and return a new user for testing

    Args:
        email (str, optional): email for the new user. Defaults to 'email@sample.com'.
        password (str, optional): password for the new user. Defaults to 'test123'.
    """
    return get_user_model().objects.create_user(email, password)


#


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful
        """
        email = "test@example.com"
        password = "somepassword123"
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test if the email for a new user is normalized
        """
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "test123")

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """
        Test creating user without an email raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """
        Test creating a new superuser
        """
        user = get_user_model().objects.create_superuser("test@example.com", "test123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
