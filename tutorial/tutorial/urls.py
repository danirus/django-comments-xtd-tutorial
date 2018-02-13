from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'blog/', include('blog.urls', namespace='blog')),
    path(r'comments/', include('django_comments_xtd.urls')),
    path(r'', TemplateView.as_view(template_name="home.html"),
        name='homepage'),
    path(r'jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
