"""
URL mappings for the user API.
"""

# Django
from django.urls import path

# Views
from . import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("login/", views.LoginView.as_view(), name="login"),
]
