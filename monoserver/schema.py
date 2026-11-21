import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from monoserver.queries.user_query import UserQuery
from monoserver.queries.account_query import AccountQuery
from monoserver.queries.channel_query import ChannelQuery
from monoserver.queries.message_query import MessageQuery

from monoserver.mutations.account_mutation import AccountMutation
from monoserver.mutations.channel_mutation import ChannelMutation
from monoserver.mutations.message_mutation import MessageMutation


@strawberry.type
class Query(UserQuery, AccountQuery, ChannelQuery, MessageQuery):
    pass


@strawberry.type
class Mutation(AccountMutation, ChannelMutation, MessageMutation):
    pass


schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension]
)
