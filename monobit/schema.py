import strawberry

from monobit.queries.user_query import UserQuery
from monobit.queries.account_query import AccountQuery

@strawberry.type
class Query(UserQuery, AccountQuery):
    pass


schema = strawberry.Schema(query=Query)