from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from relevation import settings

from judgementapp import views

urlpatterns = patterns('',
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'judgementapp/login.html'}, name='login_user'),
    url(r'^$', views.index, name='index'),
    url(r'^query$', views.query_list, name='all_queries'),
    url(r'^query/qrels$', views.qrels, name='query_list'),
    url(r'^query/(?P<qId>\d+)/$', views.query, name='query'),
    url(r'^query/(?P<qId>\d+)/doc/(?P<docId>[A-Za-z0-9_\-\+\.]+)/$', views.document, name='document'),
    url(r'^query/(?P<qId>\d+)/doc/(?P<docId>[+A-Za-z0-9_\-\+\.]+)/judge/$', views.judge, name='judge'),
    url(r'^about/$', views.about, name='about'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^upload/save$', views.upload,  name='upload'),
    url(r'^login/$', auth_views.login, {'template_name': 'judgementapp/login.html'}, name='login_user'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
)
