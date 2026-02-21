from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login as login_fx


from monobit.models.user import User
from monobit.views.auth.serializers import LoginSerializer, AuthenticatedUserSerializer


class AuthViewSet(ViewSet):
    @action(methods=["GET"], detail=False, url_path="me")
    def me(self, request, *args, **kwargs):
        context = {"is_authenticated": False, "authenticated_user": None}
        if request.user.is_authenticated:
            context["is_authenticated"] = True
            serializer = AuthenticatedUserSerializer(request.user)
            context["authenticated_user"] = serializer.data

        return Response(data=context, status=status.HTTP_200_OK)
