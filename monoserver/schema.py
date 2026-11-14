import strawberry

from monoserver.queries.user_query import UserQuery
from monoserver.queries.account_query import AccountQuery

from monoserver.mutations.account_mutation import AccountMutation

@strawberry.type
class Query(UserQuery, AccountQuery):
    pass

@strawberry.type
class Mutation(AccountMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)