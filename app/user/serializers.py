"""
Serializers for the user API View.
"""
# Django
from django.contrib.auth import get_user_model

# DRF
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "full_name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        """
        Create and return a user with encrypted password.
        Args:
            validated_data (dict): The data to be validated.
        """
        return get_user_model().objects.create_user(**validated_data)
