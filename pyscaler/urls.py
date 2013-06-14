"""
This file contains the URL definitions for the PyScaler project. It delegates the urls of each module to its own urls file.
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from pyscaler  import views

admin.autodiscover()

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r'^monitoring/', include('apps.monitoring.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^control/', include('apps.control.urls')),
    url(r'^actions/', include('apps.actions.urls')),
    url(r'^administration/$', views.administration, name='administration'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
