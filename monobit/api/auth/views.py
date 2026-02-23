from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login as login_user


from monobit.models.user import User
from monobit.api.auth.serializers import LoginSerializer, AuthenticatedUserSerializer


class AuthViewSet(ViewSet):
    @action(methods=["GET"], detail=False, url_path="me")
    def me(self, request, *args, **kwargs):
        context = {"is_authenticated": False, "authenticated_user": None}
        if request.user.is_authenticated:
            context["is_authenticated"] = True
            serializer = AuthenticatedUserSerializer(request.user)
            context["authenticated_user"] = serializer.data

        return Response(data=context, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="login")
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_data = serializer.validated_data
        user: User = User.objects.filter(
            email_address=auth_data.get("email_address")
        ).first()
        if not user:
            return Response(
                data={"detail": "No account found with the given email address"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not user.check_password(auth_data.get("password")):
            return Response(
                data={"detail": "Invalid credentials."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_blocked:
            return Response(
                data={
                    "detail": "You'r account has been blocked. Please contact administrator for further action",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        login_user(request, user)
        return Response(data=None, status=status.HTTP_200_OK)
