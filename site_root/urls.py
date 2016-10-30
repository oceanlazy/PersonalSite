from django.conf.urls import include, url
from django.contrib import admin
from my_site import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/(?P<cur_page>\d+)?', views.index),
    url(r'^blog/(?P<cur_page>\d+)?', views.blog),
    url(r'^articles/(?P<cur_page>\d+)?', views.articles),
    url(r'^contacts/(?P<cur_page>\d+)?', views.contacts),
    url(r'^python/(?P<cur_page>\d+)?', views.python),
    url(r'^$', views.index),
]