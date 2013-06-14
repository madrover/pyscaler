"""
The **apps.actions.urls** module contains the Django urls definition for the **actions** app.

* /actions/executescript/{{script}}/cluster/{{cluster}}/node/{{node}}
    Launches the **executeScriptOnNode** views function.

* /actions/executescript/{{script}}/cluster/{{cluster}}/ 
    Launches the **executeScriptOnNode** views function.

* /actions/executescript/output/{{taskid}}/
    Launches the **executeScriptOutput** views function.

* /actions/ec2node/deploy/cluster/{{cluster}}/profile/{{ec2profile}}/sshprofile/{{sshprofile}}/jvmprofiles/{{jvmprofiles,jvmprofiles}}
    Launches the **ec2nodeDeploy** views function. **jvmprofiles** parameter can be repeated. Repetitions are split by commas.

* /actions/ec2node/remove/cluster/{{cluster}}/node/{{node}}/
    Launches the **ec2nodeRemove** views function.

* /actions/ec2node/output/{{taskid}}/
    Launches the **ec2nodeOutput** views function.
"""
from django.conf.urls import patterns, include, url
from apps.actions import views


slugpattern = "[A-Za-z0-9-_]{1,50}"
urlpatterns = patterns('',
    url(r'^executescript/(?P<script>' + slugpattern + ')/cluster/(?P<cluster>'+ slugpattern + ')/node/(?P<node>'+ slugpattern + ')/$', views.executeScriptOnNode, name='executeScriptOnNode'),
    url(r'^executescript/(?P<script>'+ slugpattern + ')/cluster/(?P<cluster>'+ slugpattern + ')/$', views.executeScriptOnCluster, name='executeScriptOnCluster'),
    url(r'^executescript/output/(?P<taskid>'+ slugpattern + ')/$', views.executeScriptOutput, name='executeScriptOutput'),
    url(r'^ec2node/deploy/cluster/(?P<cluster>'+ slugpattern + ')/profile/(?P<ec2profile>'+ slugpattern + ')/sshprofile/(?P<sshprofile>'+ slugpattern + ')/jvmprofiles/(?P<jvmprofiles>[A-Za-z0-9-_,]{1,50})/$', views.ec2nodeDeploy, name='ec2nodeDeploy'),
    url(r'^ec2node/remove/cluster/(?P<cluster>'+ slugpattern + ')/node/(?P<node>'+ slugpattern + ')/$', views.ec2nodeRemove, name='ec2nodeRemove'),
    url(r'^ec2node/output/(?P<taskid>'+ slugpattern + ')/$', views.ec2nodeOutput, name='ec2nodeOutput'),
    )

