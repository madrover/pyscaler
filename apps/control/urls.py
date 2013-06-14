"""
The **apps.control.urls** module contains the Django urls definition for the **control** app.

* /control/cluster/**cluster**/nodelist/
    Launches the **nodelist** views function.

* /control/cluster/**cluster**/triggerlist/
    Launches the **triggerlist** views function.
    
* /control/ec2nodes/
    Launches the **ec2nodes** views function.
    
* /control/ec2profile/detail/{{ec2profile**)/
    Launches the **ec2profileDetail** views function.
    
* /control/distributedscripts/
    Launches the **distributedscripts** views function.
    
* /control/localscripts/
    Launches the* *localscripts** views function.
    
* /control/triggers/
    Launches the **triggers** views function.
    
* /control/trigger/{{trigger}}/actionlist/
    Launches the **triggerActionList** views function.
    
* /control/trigger/{{trigger}}/execute/
    Launches the **triggerExecute** views function.
    
* /control/trigger/output/**taskid**/
    Launches the **triggerOutput** views function.


"""
from django.conf.urls import patterns, include, url
from apps.control import views


slugpattern = "[A-Za-z0-9-_]{1,50}"
urlpatterns = patterns('',
    url(r'^cluster/(?P<cluster>'+ slugpattern + ')/nodelist/$', views.nodelist, name='nodelist'),
    url(r'^cluster/(?P<cluster>'+ slugpattern + ')/triggerlist/$', views.triggerlist, name='triggerlist'),
    url(r'^ec2nodes/$', views.ec2nodes, name='ec2nodes'),
    url(r'^ec2profile/detail/(?P<ec2profile>'+ slugpattern + ')/$', views.ec2profileDetail, name='ec2profileDetail'),
    url(r'^distributedscripts/$', views.distributedscripts, name='distributedscripts'),
    url(r'^localscripts/$', views.localscripts, name='localscripts'),
    url(r'^triggers/$', views.triggers, name='triggers'),
    url(r'^trigger/(?P<trigger>'+ slugpattern + ')/actionlist/$', views.triggerActionList, name='triggerActionList'),
    url(r'^trigger/(?P<trigger>'+ slugpattern + ')/execute/$', views.triggerExecute, name='triggerExecute'),
    url(r'^trigger/output/(?P<taskid>'+ slugpattern + ')/$', views.triggerOutput, name='triggerOutput'),
    
)

