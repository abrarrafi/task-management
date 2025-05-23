from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # include app-specific urls
    path('tasks/', include('tasks.urls')),

]

# Serve static and media files in development
if settings.DEBUG:
    print("Adding static and media URL handlers")  # Debug print
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

