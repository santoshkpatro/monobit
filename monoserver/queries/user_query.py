import strawberry

from monoserver.types import UserType
from monoserver.models import User
from monoserver.permissions import IsAuthenticated


@strawberry.type
class UserQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    def users(self) -> list[UserType]:
        return User.objects.all()
