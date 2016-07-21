from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = "boards"
urlpatterns = [
    url(r'^$', views.BoardList.as_view(), name='index'),

    url(r'^(?P<slug>[\w-]+)/catalog$', views.BoardDetail.as_view(),
        name='board-detail'),

    url(r'^(?P<slug>[\w-]+)/catalog/create-thread$', views.ThreadCreate.as_view(),
        name='create-thread'),

    url(r'^(?P<slug>[\w-]+)/thread/(?P<pk>[0-9]+)$', views.ThreadDetail.as_view(),
        name='thread-detail'),

    url(r'^(?P<slug>[\w-]+)/thread/(?P<pk>[0-9]+)/reply$', views.ReplyCreate.as_view(),
        name='thread-reply'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
