import mimetypes

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
import tutorhunt.settings as settings

mimetypes.add_type("application/javascript", ".js", True)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("timeline/", include("graphics.urls")),
    path("auth/", include("users.urls")),
    path("notifications/", include("notifications.urls")),
    path("work/", include("hometasks.urls")),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
