from django.conf.urls import include, url
from django.contrib import admin
from my_site import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', views.blog),
    url(r'', views.index),
]
