from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^/?', include('tys_webapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
