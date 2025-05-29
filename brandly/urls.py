from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/kullanici/', include('kullanici.urls')),
    path('api/analiz/', include('analiz.urls')),

    # API üzerinden statik dosyaları erişmek için özel route
    re_path(r'^api/static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
]

# Geliştirme ortamında statik ve medya dosyalarını servis etmek için
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
