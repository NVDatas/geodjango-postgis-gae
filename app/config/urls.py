from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from config import settings

admin.autodiscover()

drf_yasg_schema_view = get_schema_view(
    openapi.Info(
        title='Geo API',
        default_version='v1'
    ),
    public=False,
)
drf_yasg_urls = [
    url(
        r'^swagger(?P<format>.json|.yaml)$',
        drf_yasg_schema_view.without_ui(cache_timeout=None),
        name='schema-json'
    ),
    url(
        r'^swagger/$',
        drf_yasg_schema_view.with_ui('swagger', cache_timeout=None),
        name='schema-swagger-ui'
    ),
    url(
        r'^redoc/$',
        drf_yasg_schema_view.with_ui('redoc', cache_timeout=None),
        name='schema-redoc'
    ),
]

api_v1_urls = [
    url(r'^geo/', include('geo_japan.urls')),
]

urlpatterns = [
                  url(
                      r'^$',
                      RedirectView.as_view(url='/api/docs/swagger/', permanent=True)
                  ),
                  url(
                      r'^favicon\.ico$',
                      RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'), permanent=True)
                  ),
                  url(
                      r'^robots\.txt$',
                      RedirectView.as_view(url=staticfiles_storage.url('robots.txt'), permanent=True)
                  ),

                  # admin
                  url(r'^admin/', admin.site.urls),

                  # drf-yasg
                  url(r'^api/docs/', include(drf_yasg_urls)),

                  # api
                  url(r'^api/v1/', include((api_v1_urls, 'v1'))),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
