from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^$', TemplateView.as_view(template_name="home.html"),
        name='homepage'),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
