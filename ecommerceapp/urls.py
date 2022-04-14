
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from ecommerceapp.settings import DEBUG, MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('', include('main.urls')),
    path('catalog/', include('catalog.urls')),
    path('admin/', admin.site.urls),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
