import pytest
from django.contrib.auth import get_user_model
from monobit.models import Project

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email_address="owner@test.com", full_name="Owner", password="pass1234"
    )


@pytest.fixture
def another_user():
    return User.objects.create_user(
        email_address="another@test.com", full_name="Another", password="pass1234"
    )


@pytest.fixture
def project(user):
    return Project.bootstrap(owner=user, name="Test Project")
