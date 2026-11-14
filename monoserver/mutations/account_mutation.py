import strawberry
from django.contrib.auth import login
from strawberry.types import Info
from graphql import GraphQLError

from monoserver.types import UserType
from monoserver.models import User

@strawberry.type
class AccountMutation:

    @strawberry.mutation
    def account_login(self, info: Info, email_address: str, password: str) -> UserType:
        email_address = email_address.lower().strip()
        user = User.objects.filter(email_address=email_address).first()
        if not user:
            raise GraphQLError("No account found with the given email address.")

        if not user.check_password(password):
            raise GraphQLError("Invalid password entered.")

        login(info.context.request, user)

        return user