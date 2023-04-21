"""
Views for the user API.
"""
# DRF
from rest_framework import generics

# Serializers
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer
