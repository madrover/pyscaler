"""
This file contains the URL definitions for the jmx module
"""
from django.conf.urls import patterns, url
from apps.monitoring.jmx import views

slugpattern = "[A-Za-z0-9-_]{1,50}"
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^node/(?P<node>' + slugpattern + ')/$', views.node, name='node'),
    url(r'^cluster/(?P<cluster>' + slugpattern + ')/$', views.cluster, name='cluster'),
    url(r'^jvm/(?P<node>' + slugpattern + ')/(?P<jvm>' + slugpattern + ')/$', views.jvm,name='jvm'),
    url(r'^node/(?P<node>' + slugpattern + ')/(?P<counter>' + slugpattern + ')/$', views.nodeCounterValues, name='nodeCounterValues'),
    url(r'^cluster/(?P<cluster>' + slugpattern + ')/(?P<counter>' + slugpattern + ')/$', views.clusterCounterValues, name='clusterCounterValues'),
    url(r'^jvm/(?P<node>' + slugpattern + ')/(?P<jvm>' + slugpattern + ')/(?P<counter>' + slugpattern + ')/$', views.jvmCounterValues,name='jvmCounterValues'),
)
