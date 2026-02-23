from django.db import models, transaction
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import timedelta
from django.core.exceptions import ValidationError


from monobit.models.base import BaseUUIDTimestampModel
from monobit.models.choices import (
    ProjectPlatformChoices,
    ProjectStatusChoices,
    ProjectMemberRoleChoices,
)


class Project(BaseUUIDTimestampModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    application_url = models.URLField(blank=True, null=True)
    ingest_key = models.CharField(max_length=32, blank=True, unique=True)
    platform = models.CharField(
        max_length=32,
        choices=ProjectPlatformChoices.choices,
        default=ProjectPlatformChoices.UNKNOWN,
    )
    status = models.CharField(
        max_length=32, choices=ProjectStatusChoices, default=ProjectStatusChoices.ACTIVE
    )
    archived_at = models.DateTimeField(blank=True, null=True)

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProjectMember",
        through_fields=["project", "user"],
        related_name="projects",
    )

    class Meta:
        db_table = "projects"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.ingest_key = get_random_string(12).lower()
        return super().save(*args, **kwargs)

    @classmethod
    @transaction.atomic
    def bootstrap(cls, owner, **new_project_data):
        project = cls(**new_project_data)
        project.save()
        project.memberships.create(user=owner, role=ProjectMemberRoleChoices.OWNER)
        return project

    @transaction.atomic
    def invite_project_member(self, email, invited_by, role=None):
        if role is None:
            role = ProjectMemberRoleChoices.COLLABORATOR

        if self.members.filter(email_address=email).exists():
            raise ValueError("User already a project member")

        expires_at = timezone.now() + timedelta(days=7)

        invitation = self.invitations.filter(
            email=email, invited_by=invited_by, accepted_at__isnull=True
        ).first()

        if invitation:
            invitation.expires_at = expires_at
            invitation.role = role
            invitation.save(update_fields=["expires_at", "role"])
            return invitation

        new_invitation = ProjectInvitation.objects.create(
            project=self,
            email=email,
            role=role,
            invited_by=invited_by,
            expires_at=expires_at,
        )
        return new_invitation


class ProjectMember(BaseUUIDTimestampModel):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_memberships",
    )
    role = models.CharField(
        max_length=32,
        choices=ProjectMemberRoleChoices.choices,
        default=ProjectMemberRoleChoices.COLLABORATOR,
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_project_invites",
    )

    class Meta:
        db_table = "project_members"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"], name="unique_project_user_memberships"
            )
        ]


class ProjectInvitation(BaseUUIDTimestampModel):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField()
    role = models.CharField(
        max_length=32,
        choices=ProjectMemberRoleChoices.choices,
        default=ProjectMemberRoleChoices.COLLABORATOR,
    )
    token = models.CharField(max_length=64, unique=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "project_invitations"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "email"],
                condition=Q(accepted_at__isnull=True),
                name="unique_active_invite_per_project_email",
            )
        ]

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.token = get_random_string(32)
        return super().save(*args, **kwargs)

    @transaction.atomic
    def accept(self, user):
        # Lock row to prevent race conditions
        invitation = ProjectInvitation.objects.select_for_update().get(id=self.id)
        if invitation.accepted_at:
            raise ValidationError("Invitation is already accepted!")

        if invitation.expires_at < timezone.now():
            raise ValidationError("Invitation expired")

        if user.email_address.lower() != invitation.email.lower():
            raise ValidationError("Invitation email mismatch")

        membership = ProjectMember(
            project=self.project, user=user, role=self.role, invited_by=self.invited_by
        )
        membership.save()

        invitation.accepted_at = timezone.now()
        invitation.save(update_fields=["accepted_at"])

        return membership
