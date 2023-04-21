"""
URL mappings for the user API.
"""

# Django
from django.urls import path

# Views
from user import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
]
