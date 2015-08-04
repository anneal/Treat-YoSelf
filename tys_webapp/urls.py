from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^welcome/?$', views.welcomePage, name='welcome'),
    url(r'^oauthlogin/?$', views.oauthLogin, name='oauth'),
    url(r'^logout/?$', views.logout_view, name='logout')
]
