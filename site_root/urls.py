from django.conf.urls import include, url
from django.contrib import admin
from my_site import views
from . import settings
from django.views.static import serve

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/(?P<cur_page>\d+)?', views.index),
    url(r'^blog/(?P<cur_page>\d+)?', views.blog),
    url(r'^publication/(?P<slug>[\w-]+)', views.publication),
    url(r'^contacts', views.contacts),
    url(r'^articles/(?P<slug_1>[\w]+)?/?(?P<slug_2>[\w]+)?/?(?P<page>[\d+]+)?', views.articles),
    url(r'^$', views.index),
]
