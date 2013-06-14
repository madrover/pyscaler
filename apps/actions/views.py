"""
| The **apps.actions.views** module contains the Django views definitions for the **actions** app.
| These views handles the actions requests and their answers. All answers of these views are JSON and are meant to be used as an API.
"""
from django.http import HttpResponse
from apps.control.models import Cluster, Node,Ec2Profile,SshProfile,JvmProfile
from apps.actions.models import Action
from django.shortcuts import get_object_or_404
from apps.actions import tasks
from django.utils.simplejson import dumps
from django.contrib.auth.decorators import login_required
from celery.result import AsyncResult 

@login_required
def executeScriptOnCluster(request,cluster,script):
    """
    | The **executeScriptOnCluster** function is used to execute a **DistributedScript** or **LocalScript** on a **Cluster**.
    | It uses the **executeScriptTask** function to execute the script.
    """
    cluster = get_object_or_404(Cluster,name=cluster)
    return executeScriptTask(cluster,script)
    
@login_required
def executeScriptOnNode(request,cluster,node,script):
    """
    | The **executeScriptOnNode** function is used to execute a **DistributedScript** or **LocalScript** on a **Node**.
    | It uses the **executeScriptTask** function to execute the script. 
    """
    cluster = get_object_or_404(Cluster,name=cluster)
    node = get_object_or_404(Node,name=node,cluster__name=cluster)
    return executeScriptTask(node,script)
 
def executeScriptTask(destination,script):
    """
    | The **executeScriptTask** function is executed by the **executeOnNode** and **executeOnCluster** function views to execute a **DistributedScript** or **LocalScript** on a specific destination.
    | Its output is a JSON object containing the id of the Celery task that is executing the script.
    """
    script = get_object_or_404(Action,name=script)
    script = Action.objects.get_subclass(name=script)
    task = tasks.executeScript.delay(destination,script)
    
    return HttpResponse(dumps({'taskid':task.id}), 'application/json')

@login_required
def executeScriptOutput(request,taskid):
    """
    The  **executeScriptOutput** function returns the status and output for the Celery task used to execute a **DistributedScript** or **LocalScript** in JSON format
    """
    result = AsyncResult(taskid)
    
    return HttpResponse(dumps({'taskid':taskid,'state':result.state,'result':result.result}), 'application/json')


@login_required
def ec2nodeDeploy(request,cluster,ec2profile,sshprofile,jvmprofiles):
    """
    | The **ec2nodeDeploy** function will launch an ec2 instance using a **Ec2Profile**, a **SshProfile** and many **JvmProfiles** and will add it to the specifed **Cluster**.
    | It needs **AWSAccessKeyId** and **AWSSecretKey** to be defined in Django's **settings.py**
    | Its output is a JSON object containing the id of the Celery task that is executing deploying the EC2 **Node**.
    """
    cluster = get_object_or_404(Cluster, name=cluster)
    ec2profile = get_object_or_404(Ec2Profile, name=ec2profile)
    sshprofile = get_object_or_404(SshProfile, name=sshprofile)
    jvmlist = []
    for jvmprofile in jvmprofiles.split(","):
        jvmprofile = get_object_or_404(JvmProfile, name=jvmprofile)
        jvmlist.append(jvmprofile)
    jvmprofiles = jvmlist
    task = tasks.ec2nodeDeploy.delay(cluster,ec2profile,sshprofile,jvmprofiles)

    return HttpResponse(dumps({'taskid':task.id}), 'application/json')
   

@login_required
def ec2nodeRemove(request,cluster,node):
    """
    | This view function will remove a Node from PyScaler and terminate the ec2 instance.
    | It needs **AWSAccessKeyId** and **AWSSecretKey** to be defined in Django's **settings.py**
    
    """
    cluster = get_object_or_404(Cluster, name=cluster)
    node = get_object_or_404(Node, name=node,cluster__name=cluster.name)
   
    task = tasks.ec2nodeRemove.delay(cluster,node)
    
    return HttpResponse(dumps({'taskid':task.id}), 'application/json')

@login_required
def  ec2nodeOutput(request,taskid):
    """
    The **ec2nodeOutput** function returns the status and output for the Celery task used to deploy or remove an Ec2 **Node** in JSON format.
    """
    result = AsyncResult(taskid)
    
    return HttpResponse(dumps({'taskid':taskid,'state':result.state,'result':result.result}), 'application/json')
