from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from monobit.schema import schema
from monobit.views.accounts import AccountsLoginView

# fmt: off
urlpatterns = [
    path("accounts/login/", AccountsLoginView.as_view(), name="accounts/login"),
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql")
]
