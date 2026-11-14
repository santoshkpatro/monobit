import strawberry
import strawberry_django
from enum import Enum

from monoserver.models import User, Message, Channel

import strawberry


@strawberry.enum
class ChannelVisibilityEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    OPEN = "open"
    DIRECT = "direct"


@strawberry_django.type(User)
class UserType:
    id: str
    username: str
    email_address: str
    full_name: str
    display_name: str
    identity_type: str
    is_admin: bool


@strawberry.type
class AccountStatusType:
    is_logged_in: bool
    logged_in_user: UserType | None


@strawberry_django.type(Channel)
class ChannelType:
    id: str
    owner: UserType
    owner_id: str
    name: str
    visibility: ChannelVisibilityEnum


@strawberry_django.type(Message)
class MessageType:
    channel_id: str
    channel: ChannelType
    id: str
    sender: UserType
    content: str
    parent_id: str
