import strawberry
from strawberry.types import Info
from graphql import GraphQLError
from django.db import transaction


from monoserver.models import Channel, ChannelMembership, ChannelMembershipRole
from monoserver.types import ChannelVisibilityEnum, ChannelType
from monoserver.permissions import IsAuthenticated


@strawberry.type
class ChannelMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
    def create_channel(
        self, info: Info, name: str, visibility: ChannelVisibilityEnum
    ) -> ChannelType:
        owner = info.context.request.user
        channel = Channel.objects.create(name=name, owner=owner, visibility=visibility)
        ChannelMembership.objects.create(
            user=owner, channel=channel, role=ChannelMembershipRole.ADMIN
        )
        return channel
