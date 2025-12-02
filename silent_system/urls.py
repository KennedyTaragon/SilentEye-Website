from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Put the admin path first
    path('admin/', admin.site.urls), 
    
    # 2. Include the app URLs
    path('', include('website.urls')),
]

# 3. Only add the media serving lines in DEBUG mode, 
#    and leave out the STATIC_URL one if possible.
if settings.DEBUG:
    # The runserver command handles STATIC_URL automatically.
    # We only explicitly add MEDIA_URL here.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

# Delete the line below (if it exists) from your root urls.py:
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)