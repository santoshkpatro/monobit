from django.contrib import admin
from django.urls import path, re_path
from monobit.views.base import index

urlpatterns = [
    path("admin/", admin.site.urls),
    # Catch-all for SPA
    re_path(r"^(?!admin/).*", index, name="index"),
]
