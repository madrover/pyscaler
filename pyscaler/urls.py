"""
This file contains the URL definitions for the PyScaler project. It delegates the urls of each module to its own urls file.


Available URLs:

* **/** This url definition is implemented in pyscaler.views.index and is shows the homepage
* **/admin** This url goes to the Django native adminstration pages
* **/account** This url definition is an included for the urls to be implemented in the account module
* **/grappelli** This url definition is an included for the urls to be implemented in the grappelli module
* **/monitoring** This url definition is an included for the urls to be implemented in the monitoring module
* **/control** This url definition is an included for the urls to be implemented in the control module
* **/actions** This url definition is an included for the urls to be implemented in the actions module
* **/administration** This url definition is implemented in pyscaler.views.administration and integrated Django admin pages into Pyscaler user interface
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
