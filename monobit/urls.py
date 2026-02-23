from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from monobit.views.base import index, ConfigAPIView
from monobit.views.auth.views import AuthViewSet
from monobit.views.projects.views import ProjectViewSet

router = SimpleRouter(trailing_slash=False, use_regex_path=True)

router.register("auth", AuthViewSet, basename="auth")
router.register("projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/config", ConfigAPIView.as_view(), name="config"),
    path("api/", include(router.urls)),
    # Catch-all for SPA
    re_path(r"^(?!admin/).*", index, name="index"),
]
