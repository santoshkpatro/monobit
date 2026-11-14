import strawberry
import strawberry_django

from monobit.models import User


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