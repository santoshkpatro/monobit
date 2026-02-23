from django.db import models


class UserRoleChoices(models.TextChoices):
    ADMIN = ("admin", "Admin")
    OWNER = ("owner", "Owner")
    STAFF = ("staff", "Staff")


class ProjectPlatformChoices(models.TextChoices):
    PYTHON = ("python", "Python")
    JAVASCRIPT = ("javascript", "JavaScript")
    RUBY = ("ruby", "Ruby")
    JAVA = ("java", "Java")
    DOTNET = ("dotnet", ".NET")
    UNKNOWN = ("unknown", "Unknown")


class ProjectStatusChoices(models.TextChoices):
    ACTIVE = ("active", "Active")
    ARCHIVED = ("archived", "Archived")


class ProjectMemberRoleChoices(models.TextChoices):
    OWNER = ("owner", "Owner")
    ADMIN = ("admin", "Admin")
    COLLABORATOR = ("collaborator", "Collaborator")
