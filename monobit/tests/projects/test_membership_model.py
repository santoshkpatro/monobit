import pytest
from django.db import IntegrityError
from monobit.models.choices import ProjectMemberRoleChoices
from monobit.models.project import ProjectMember


@pytest.mark.django_db
def test_unique_project_user_membership_constraint(project, another_user):
    ProjectMember.objects.create(
        project=project,
        user=another_user,
        role=ProjectMemberRoleChoices.COLLABORATOR,
    )

    with pytest.raises(IntegrityError):
        ProjectMember.objects.create(
            project=project,
            user=another_user,
            role=ProjectMemberRoleChoices.COLLABORATOR,
        )
