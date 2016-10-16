from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = "boards"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(
        r'^(?P<slug>[\w-]+)/catalog/$',
        views.board_detail,
        name='board-detail'
    ),
    url(
        r'^thread-delete/(?P<pk>[0-9]+)/$',
        views.thread_delete,
        name='thread-delete'
    ),
    url(
        r'^(?P<slug>[\w-]+)/thread/(?P<pk>[0-9]+)/$',
        views.thread_view,
        name='thread-detail'
    ),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
