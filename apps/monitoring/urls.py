"""
This file contains the URL definitions for the monitoring module.

Available URLs:

* **/monitoring** This url definition is implemented in apps.monitoring.views.index and is just a pass through to the specific monitoring modules
* **/monitoring/jmx** This url definition is an included for the urls to be implemented in the jmx module
* **/monitoring/ssh** This url definition is an included for the urls to be implemented in the ssh module

"""
from django.conf.urls import patterns, include, url
from apps.monitoring import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^jmx/', include('apps.monitoring.jmx.urls')),
    url(r'^ssh/', include('apps.monitoring.ssh.urls')),
)

