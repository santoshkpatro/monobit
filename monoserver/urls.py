from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from monoserver.schema import schema
from monoserver.views import SSERelayView

# fmt: off
urlpatterns = [
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql"),
    path("sse/relay/", SSERelayView.as_view(), name="sse-relay")
]
