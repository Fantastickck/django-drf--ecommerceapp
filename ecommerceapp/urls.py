
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from ecommerceapp.settings import DEBUG, MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('', include('main.urls')),
    path('catalog/', include('catalog.urls')),
    path('cart/', include('cart.urls')),
    path('', include('user_product.urls')),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]

if DEBUG:
    import debug_toolbar

    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    urlpatterns = [
                      path('debug/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
