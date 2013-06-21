"""
| The **apps.monitoring.ssh.views** module contains the Django views definitions for the **ssh** app.
| These views mainly handle the PyScaler web frontend.
"""
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.utils import simplejson

from apps.control.models import Cluster, Node
from apps.monitoring.ssh.models import SshCounter
from apps.monitoring.ssh.tasks import getSshTriggerCounters
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from django.core import serializers
import datetime,time


def index(request):
    """
    The **index** function is to as an entry to the **SshCounter** graphs pages. It uses the **ssh.html** template.
    """
    clusters = Cluster.objects.select_related().all()
    context = Context({
        'clusters': clusters,
    })
    return render(request, 'ssh.html',context)

def node(request,node):
    node = get_object_or_404(Node,name=node)
    context = Context({'node': node,})
    #Gather associated triggers
    triggers = node.cluster.triggers.all()
    for trigger in triggers:
        getSshTriggerCounters.delay(node,trigger)
    
    counterdata = []
    for trigger in triggers:
        counters = trigger.counters.all().select_subclasses()
        for counter in counters:
            if isinstance(counter, SshCounter):
                counterdata.append(counter)
    context.update( {'counters':counterdata})
    return render(request, 'sshnode.html',context)

def cluster(request,cluster):
    """
    The **cluster** view shows SSH graphs for a specific Cluster.
    """
    # Validate if cluster extsts
    cluster = get_object_or_404(Cluster,name=cluster)
    context = Context({'cluster': cluster,})
    #Gather associated triggers
    triggers = cluster.triggers.all()
    context['triggers'] = triggers
    #Gather associated nodes
    nodes = cluster.nodes.all()
    context['nodes'] = nodes

    # Executes associated node triggers
    for node in nodes:
        for trigger in triggers:
            getSshTriggerCounters.delay(node,trigger)
            
    # Gather associated counters
    counterdata = []
    for trigger in triggers:
        counters = trigger.counters.all().select_subclasses()
        for counter in counters:
            if isinstance(counter, SshCounter):
                counterdata.append(counter)
    context.update( {'counters':counterdata})
    
    return render(request, 'sshcluster.html',context)

def SshCounterData(node,counter):
    """
    The **SshCounterData** function connects to memcached and gathers last 24 hours performance data for a specific counter
    """
    now = datetime.datetime.now()
    utcnow = datetime.datetime.utcnow()
    #print now
    #print utcnow
    key = 'ssh_sshcounter.' +  str(node.pk) + '.' +  str(counter.pk) + '.'
    epochkeysdict = {}
    for i in xrange(1440,1,-1):#1440,1,-1):
        td=datetime.timedelta(minutes=1)
        difference = now - (i * td)
        #print str(difference) + " " + str( time.mktime(difference.timetuple()))
        ckey = key + difference.strftime('%Y%m%d%H%M')
        utcdifference = utcnow - (i * td)
        #print str(utcdifference) + " " + str( time.mktime(utcdifference.timetuple()))
        # Flot expects javascript format (epoch in ms)
        epoch= time.mktime(difference.timetuple()) * 1000
        #print epoch
        epochkeysdict[epoch]=ckey
        
    
    cachedict = cache.get_many(epochkeysdict.values())
    for epochkey in epochkeysdict.items():
        key = epochkey[0]
        value = epochkey[1]
        if cachedict.has_key(value):
            epochkeysdict[key]=cachedict[value]
        else:
            epochkeysdict[key]="null"
    
    return sorted(epochkeysdict.items())


def clusterCounterValues(request,cluster,counter):
    """
    The **clusterCounterValues** view returns last 24h of performance data for a specific Cluster and Counter in JSON format,
    """
    try:
        cluster = Cluster.objects.get(name__exact=cluster)
    except Cluster.DoesNotExist:
        return HttpResponse(simplejson.dumps({}),mimetype="application/json")
    triggers = cluster.triggers.all()
    
    c=""
    for trigger in triggers:
        try:
            c = trigger.counters.get(name__exact=counter)
        except:
            pass
        if c !="":
            break
    counter = c
    if counter == "":
        return HttpResponse(simplejson.dumps({}),mimetype="application/json")
    nodes = cluster.nodes.all()
    data_out = ""
    for node in nodes:
            data = SshCounterData(node,counter)
            data_dict = {"label":node.name,"data":data}
            data_out = data_out + "," + simplejson.dumps(data_dict)
    data_out = "[" + data_out[1:] + "]"
    return HttpResponse(data_out,mimetype="application/json")

def nodeCounterValues(request,node,counter):
    """
    The **nodeCounterValues** view returns last 24h of performance data for a specific Node and Counter in JSON format,
    """
    try:
        node = Node.objects.get(name__exact=node)
    except Node.DoesNotExist:
        return HttpResponse(simplejson.dumps({}),mimetype="application/json")
    triggers = node.cluster.triggers.all()
    c=""
    for trigger in triggers:
        try:
            c = trigger.counters.get(name__exact=counter)
        except:
            pass
        if c !="":
            break
    counter = c
    if counter == "":
        return HttpResponse(simplejson.dumps({}),mimetype="application/json")
    data = SshCounterData(node,counter)
    data_dict = {"label":node.name,"data":data}
    data_out = simplejson.dumps(data_dict)
    data_out = "[" + data_out + "]"
    return HttpResponse(data_out,mimetype="application/json")
