"""
| The **apps.monitoring.jmx.views** module contains the Django views definitions for the **jmx** app.
"""
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django import forms
from apps.control.models import Cluster, Node,Trigger
from apps.actions.models import Action,DistributedScript,LocalScript,Ec2Profile,SshProfile,JvmProfile,TriggerAction, OSConfiguration
from django.shortcuts import get_object_or_404
from apps.actions.tasks import executeViaFabric
from apps.control import tasks
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.contrib.auth.decorators import login_required
from apps.actions.tasks import executeViaFabric,ec2nodeDeploy,ec2nodeRemove
from apps.actions.models import TriggerAction,Action,Email,OSConfiguration,LocalScript,DistributedScript,DeployEc2Node
from celery import chain
from celery.result import AsyncResult

@login_required
def nodelist(request,cluster):
    """
    The **nodelist** function returns the **Node** list for a specific **Cluster** in JSON format
    """
    cluster = get_object_or_404(Cluster.objects.select_related(), name=cluster)
    nodes = []
    for node in cluster.nodes.all():
        nodes.append(node.name)

    return HttpResponse(dumps({'nodes':nodes}), 'application/json')

@login_required
def triggerlist(request,cluster):
    """
    The **triggerlist** function returns the **Trigger** list for a specific **Cluster** in JSON format
    """
    cluster = get_object_or_404(Cluster.objects.select_related(), name=cluster)
    triggers = []
    for trigger in cluster.triggers.all():
        triggers.append(trigger.name)

    return HttpResponse(dumps({'triggers':triggers}), 'application/json')


# @login_required
# def executeOutput(request,taskid):
#     """
#     The **executeOutput** function returns the status and output for a specific Celery task in JSON format
#     """
#     result = AsyncResult(taskid)
#     
#     return HttpResponse(dumps({'taskid':taskid,'state':result.state,'result':result.result}), 'application/json')

@login_required
def ec2nodes(request):
    """
    The **ec2nodes** function is used display the Ec2 Nodes management page on the frontend web page. It uses the **ec2nodes.html** template.
    """
    clusters = Cluster.objects.select_related().all()
    ec2profiles = Ec2Profile.objects.all()
    sshprofiles = SshProfile.objects.all()
    jvmprofiles = JvmProfile.objects.all()
    
    context = Context({
        'clusters': clusters,
        'ec2profiles':ec2profiles,
        'sshprofiles': sshprofiles,
        'jvmprofiles':jvmprofiles,
    })
    return render(request, 'ec2nodes.html',context)

@login_required
def osprovisioning(request):
    """
    The **osprovisioning** function is used display the **OSConfiguration** deployment  page on the frontend web page. It uses the **execute.html** template.
    """
    clusters = Cluster.objects.select_related().all()
    osconfigurations = OSConfiguration.objects.all()
    context = Context({
        'clusters': clusters,
        'osconfigurations':osconfigurations,
    })
    return render(request, 'execute.html',context)

@login_required
def localscripts(request):
    """
    The **localscripts** function is used display the **LocalScript** execution  page on the frontend web page. It uses the **execute.html** template.
    """
    clusters = Cluster.objects.select_related().all()
    localscripts = LocalScript.objects.all()
    context = Context({
        'clusters': clusters,
        'localscripts':localscripts,
    })
    return render(request, 'execute.html',context)

@login_required
def distributedscripts(request):
    """
    The **distributedscripts** function is used display the **DistributedScript** execution  page on the frontend web page. It uses the **execute.html** template.
    """
    clusters = Cluster.objects.select_related().all()
    distributedscripts = DistributedScript.objects.all()
    context = Context({
        'clusters': clusters,
        'distributedscripts':distributedscripts,
    })
    return render(request, 'execute.html',context)


@login_required
def ec2profileDetail(request,ec2profile):
    """
    The **ec2profileDetail** function returns a dictionary of an **Ec2Profile** model fields and values in JSON format.
    """
    ec2profile = get_object_or_404(Ec2Profile, name=ec2profile)
    nodeDetail ={
                 'name': ec2profile.name,
                 }
    fields = Ec2Profile._meta.get_all_field_names()
    for field in fields:
        if field not in ['action_ptr', 'actions', 'id', 'node','deployec2node']:
            nodeDetail[field]=getattr(ec2profile,field)
    return HttpResponse(dumps(nodeDetail), 'application/json')

@login_required
def triggers(request):
    """
    This view function displays can be used to execute associated **ActionOrder** from a **Trigger**
    | The **triggers** function is used display the **Trigger** execution  page on the frontend web page. It can be used to execute all the **Actions** associated with a **Trigger**.
    | The **Trigger** is related to each **Action** via an **ActionOrder** that specifies the execution order and the **Action** target.
    | It  uses the **triggers.html** template.
    """
    clusters = Cluster.objects.select_related().all()
    distributedscripts = DistributedScript.objects.all()
    context = Context({
        'clusters': clusters,
    })
    return render(request, 'triggers.html',context)


@login_required
def triggerActionList(request,trigger):
    """
    The **triggerlist** function returns the **Actions** list for a specific **Trigger** in JSON format
    """
    trigger = get_object_or_404(Trigger.objects.select_related(), name=trigger)
    triggeractions = TriggerAction.objects.filter(trigger=trigger).order_by('order')
    
    actions = []
    for triggeraction in triggeractions:
        actions.append([triggeraction.order,triggeraction.action.name])

    return HttpResponse(dumps({'actions':actions}), 'application/json')

@login_required
def triggerExecute(request,trigger):
    """
    The **triggerExecute** view executes a **Trigger** associated with a **Cluster**.
    
    It executes each associated **Action** in the order specified in the **TriggerAction** intermediate model Order field.
    
    It uses as destination of each **Action** the targer specified in the Target field.
    
    It can be:
    
    - CLUSTER, the **Cluster** associated to the **Trigger**. Can be used by **DeployEc2Node**, **OSConfiguration**, **LocalScript** and **DistributedScript** actions.
    - LASTNODE, the last created **Node** of the **Cluster** associated to the **Trigger**. Can be used by **OSConfiguration**, **LocalScript** and **DistributedScript** actions.
    - NONE, no specified target. Can be used by **Email** action.
    """
    trigger = get_object_or_404(Trigger.objects.select_related(), name=trigger)
    
    # Check if trigger == Trigger or String?
    if not isinstance(trigger, Trigger):
        trigger = Trigger.objects.get(name=trigger)
    cluster = trigger.cluster
    for n in Node.objects.filter(cluster=cluster).select_related()[:1]:
        lastnode =n 
    triggeractions = TriggerAction.objects.filter(trigger=trigger).order_by('order')
    
    #We list the actions associated with a trigger
    actions = {}
    for triggeraction in triggeractions:
        if triggeraction.target == "cluster":
            destination = cluster
        elif triggeraction.target == "lastnode":
            destination = lastnode
        else:
            destination = "node"
        action = Action.objects.get_subclass(name=triggeraction.action.name)
        actions[triggeraction.order]={'destination':destination,'action':action}
    subtasks=[]
    
    # Get each action  associated with a trigger and create a new celery inmutable subtak to be executed
    for key in sorted(actions.iterkeys()):
        destination = actions[key]['destination']
        action = actions[key]['action']
        if isinstance(action, LocalScript):
            subtask = executeViaFabric.si(destination,action)
            subtasks.append(subtask)
        elif isinstance(action, DistributedScript):
            subtask = executeViaFabric.si(destination,action)
            subtasks.append(subtask)
        elif isinstance(action, DeployEc2Node):
            subtask = ec2nodeDeploy.si(destination,action.ec2profile,action.sshprofile,action.jvmprofiles)
            subtasks.append(subtask)
        elif isinstance(action, Email):
            pass
        elif isinstance(action, OSConfiguration):
            pass
    
    # The trigger subtasks are handed over to celery to be executed sequentially
    task = chain(*subtasks).apply_async()
    taskids=[]
    taskids.append(task.id)
    while task.parent != None:
        task=task.parent
        taskids.insert(0,task.id)
    # Orderd the tasks list
    a = 0
    tasks=[]
    for key in sorted(actions.iterkeys()):
        d={}
        d["order"]=key
        d["action"]= actions[key]["action"].name
        d["destination"]= actions[key]["destination"].name
        d["taskid"]=taskids[a]
        tasks.append(d)
        a=a+1
    return HttpResponse(dumps(tasks), 'application/json')

@login_required
def triggerOutput(request,taskid):
    """
    The  **triggerOutput** function returns the status and output for the Celery task used to execute a **Trigger** in JSON format
    """
    result = AsyncResult(taskid)
    
    return HttpResponse(dumps({'taskid':taskid,'state':result.state,'result':result.result}), 'application/json')