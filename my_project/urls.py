from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin interface
    path('', include('apps.home.urls')),  # Include home app URLs
    path('upload_form/', include('apps.upload.urls')),  # Include upload app URLs
]