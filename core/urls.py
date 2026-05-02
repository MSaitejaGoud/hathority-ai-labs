"""
Root URL configuration for the Team AI Showcase.

- `/`               -> projects homepage (list + search)
- `/project/<pk>/`  -> project detail page
- `/admin/`         -> Django Admin
- `/media/...`      -> user-uploaded files (DEBUG only)
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("projects.urls")),
]

# Serve uploaded media files in development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
