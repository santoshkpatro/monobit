from django.contrib import admin
from django.urls import path, re_path, include
from monobit.views.base import index, ConfigAPIView
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=False, use_regex_path=True)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/config", ConfigAPIView.as_view(), name="config"),
    path("api/", include(router.urls)),
    # Catch-all for SPA
    re_path(r"^(?!admin/).*", index, name="index"),
]
