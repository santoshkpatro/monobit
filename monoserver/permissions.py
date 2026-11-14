from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    message = "Log In required."

    def has_permission(self, source, info, **kwargs):
        user = info.context.request.user

        return user.is_authenticated