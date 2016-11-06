from django.conf.urls import include, url
from django.contrib import admin
from my_site import views
from . import settings
from django.views.static import serve

urlpatterns = [
    url(r'^static/(?P<path>.*)/$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^publication/(?P<slug>[\w-]+)/$', views.RecordView.as_view()),
    url(r'^contacts/$', views.AboutView.as_view()),
    url(r'^index/(?P<cur_page>\d+)?/$', views.IndexView.as_view()),
    url(r'^blog/(?P<cur_page>\d+)?/?$', views.BlogView.as_view()),
    url(r'^articles/(?P<slug_1>[\d]+)?/?$', views.ArticlesView.as_view()),
    url(r'^articles/(?P<slug_1>[\w]+)?/(?P<slug_2>[\d]+)?/?$', views.ArticlesCategoryView.as_view()),
    url(r'^articles/(?P<slug_1>[\w]+)?/(?P<slug_2>[\w]+)/?(?P<slug_3>[\d]+)?/?$', views.ArticlesSubCategoryView.as_view()),
    url(r'^$', views.IndexView.as_view()),
]
