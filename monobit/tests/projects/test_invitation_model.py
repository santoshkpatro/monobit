import pytest
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_accept_invitation_success(project, user, another_user):
    invitation = project.invite_project_member(
        email=another_user.email_address,
        invited_by=user,
    )

    membership = invitation.accept(another_user)

    assert membership.user == another_user
    assert project.memberships.filter(user=another_user).exists()

    invitation.refresh_from_db()
    assert invitation.accepted_at is not None


@pytest.mark.django_db
def test_accept_invitation_already_accepted(project, user, another_user):
    invitation = project.invite_project_member(
        email=another_user.email_address,
        invited_by=user,
    )

    invitation.accept(another_user)

    with pytest.raises(ValidationError):
        invitation.accept(another_user)


@pytest.mark.django_db
def test_accept_invitation_expired(project, user, another_user):
    invitation = project.invite_project_member(
        email=another_user.email_address,
        invited_by=user,
    )

    invitation.expires_at = timezone.now() - timedelta(days=1)
    invitation.save(update_fields=["expires_at"])

    with pytest.raises(ValidationError):
        invitation.accept(another_user)


@pytest.mark.django_db
def test_accept_invitation_email_mismatch(project, user, another_user):
    invitation = project.invite_project_member(
        email="different@test.com",
        invited_by=user,
    )

    with pytest.raises(ValidationError):
        invitation.accept(another_user)
