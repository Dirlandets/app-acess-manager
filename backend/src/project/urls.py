from django.urls import path, include, re_path
from django.contrib import admin

# STATIC
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('secret-admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'PROJECT'
admin.site.site_title = 'Администрирование'
admin.site.index_title = 'Администрирование сайта'

if settings.DEBUG:
    admin.site.site_header = 'DEVELOP ' + admin.site.site_header
    admin.site.site_title = 'DEVELOP ' + admin.site.site_title
    admin.site.index_title = 'DEVELOP ' + admin.site.index_title
