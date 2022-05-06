from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
import tutorhunt.settings as settings

urlpatterns = [
    path('timeline/', include("graphics.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
