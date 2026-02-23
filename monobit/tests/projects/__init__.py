import pytest
from monobit.models.choices import ProjectMemberRoleChoices
from monobit.models import Project


@pytest.mark.django_db
def test_ingest_key_generated_on_create():
    project = Project.objects.create(name="New Project")

    assert project.ingest_key is not None
    assert len(project.ingest_key) == 12


@pytest.mark.django_db
def test_bootstrap_creates_owner_membership(user):
    project = Project.bootstrap(owner=user, name="Boot Project")

    membership = project.memberships.first()

    assert project.memberships.count() == 1
    assert membership.user == user
    assert membership.role == ProjectMemberRoleChoices.OWNER


@pytest.mark.django_db
def test_invite_project_member_creates_invitation(project, user):
    invitation = project.invite_project_member(email="invite@test.com", invited_by=user)

    assert invitation.email_address == "invite@test.com"
    assert invitation.project == project
    assert invitation.accepted_at is None
    assert invitation.token is not None


@pytest.mark.django_db
def test_inviting_existing_member_raises_error(project, user, another_user):
    project.memberships.create(
        user=another_user,
        role=ProjectMemberRoleChoices.COLLABORATOR,
    )

    with pytest.raises(ValueError):
        project.invite_project_member(email=another_user.email_address, invited_by=user)
