from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from monoserver.schema import schema

# fmt: off
urlpatterns = [
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql")
]
