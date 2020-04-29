from django.urls import path

from . import views
from django.conf.urls import url

app_name = 'fsociety'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.chat_view, name='chat'),
    url(r'^(?P<pk>[0-9]+)/get_messages$', views.get_messages, name='get_messages'),
    url(r'^(?P<pk>[0-9]+)/set_messages$', views.set_messages, name='set_messages'),
    url(r'^logout$', views.logout_view, name="logout"),
    url(r'^login$', views.login_view, name='login'),
    url(r'^signin$', views.sign_in_form, name='sign_in'),
    url(r'^about$', views.AboutView.as_view(), name='about')
]