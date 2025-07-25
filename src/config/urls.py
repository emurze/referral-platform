from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("account.urls", namespace="account")),
    path(
        "profile/",
        include(
            "user_profile.urls",
            namespace="user_profile",
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
