import strawberry

from monobit.types import UserType, AccountStatusType
from monobit.models import User


@strawberry.type
class AccountQuery:
    @strawberry.field
    def account_status(self, info: strawberry.Info) -> AccountStatusType:
        user = info.context.request.user
        is_logged_in = user.is_authenticated

        return AccountStatusType(
            is_logged_in=is_logged_in, logged_in_user=user if is_logged_in else None
        )
