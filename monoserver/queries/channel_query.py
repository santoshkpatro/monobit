import strawberry
from strawberry.types import Info

from monoserver.permissions import IsAuthenticated
from monoserver.models import Channel
from monoserver.types import ChannelType


@strawberry.type
class ChannelQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    def list_channels(self, info: Info) -> list[ChannelType]:
        user = info.context.request.user
        channels = Channel.objects.filter(memberships__user=user)
        return channels
