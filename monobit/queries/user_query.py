import strawberry

from monobit.types import UserType
from monobit.models import User
from monobit.permissions import IsAuthenticated


@strawberry.type
class UserQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    def users(self) -> list[UserType]:
        return User.objects.all()
