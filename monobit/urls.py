from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from monobit.api.base import index, ConfigAPIView
from monobit.api.auth.views import AuthViewSet
from monobit.api.projects.views import ProjectViewSet

from monobit.ingest.view import IngestAPIView

router = SimpleRouter(trailing_slash=False, use_regex_path=True)

router.register("auth", AuthViewSet, basename="auth")
router.register("projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("ingest", IngestAPIView.as_view(), name="ingest"),
    path("admin/", admin.site.urls),
    path("api/config", ConfigAPIView.as_view(), name="config"),
    path("api/", include(router.urls)),
    # Catch-all for SPA
    re_path(r"^(?!admin/).*", index, name="index"),
]
