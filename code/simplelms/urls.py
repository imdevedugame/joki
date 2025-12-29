from django.contrib import admin
from django.urls import path, include

from core.apiv1 import apiv1      # NON JWT
from core.api import api          # JWT

urlpatterns = [
    # ADMIN & TOOL
    path("admin/", admin.site.urls),
    path("silk/", include("silk.urls", namespace="silk")),

    # HTML PAGES (HOME, STAT, dll)
    path("", include("core.urls")),

    # API (HARUS DI BAWAH & PUNYA PREFIX)
    path("api/", apiv1.urls),
    path("jwt/", api.urls),
]
