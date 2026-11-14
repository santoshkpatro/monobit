from django.db.models import TextChoices


class ChannelVisibility(TextChoices):
    PUBLIC = ("public", "Public")
    PRIVATE = ("private", "Private")
    OPEN = ("open", "Open")
    DIRECT = ("direct", "Direct")


class ChannelMembershipRole(TextChoices):
    ADMIN = ("admin", "Admin")
    COLLABORATOR = ("collaborator", "Collaborator")
    VIEWER = ("viewer", "Viewer")


class UserIdentityType(TextChoices):
    PERSON = ("person", "Person")
    GROUP = ("group", "Group")
    BOT = ("bot", "Bot")
