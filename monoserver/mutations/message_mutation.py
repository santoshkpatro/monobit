import strawberry
from strawberry.types import Info
from graphql import GraphQLError


from monoserver.models import Channel, Message, ChannelMembership
from monoserver.types import MessageType
from monoserver.permissions import IsAuthenticated


@strawberry.type
class MessageMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def send_message(self, info: Info, channel_id: str, content: str) -> MessageType:
        channel = Channel.objects.filter(id=channel_id).first()
        user = info.context.request.user
        if not channel:
            raise GraphQLError(message="Channel not found with the given channel id.")

        if not ChannelMembership.is_member(channel, user):
            raise GraphQLError(message="Unauthorized channel access.")

        message = Message.objects.create(channel=channel, sender=user, content=content)

        return message
