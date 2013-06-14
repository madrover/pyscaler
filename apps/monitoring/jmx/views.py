"""
| The **apps.control.views** module contains the Django views definitions for the **control** app.
"""
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.utils import simplejson
from apps.control.models import Cluster, Node,JvmProfile
from apps.monitoring.jmx.models import JmxCounter
from django.core.cache import cache
from django.core import serializers
import datetime,time
from django.shortcuts import get_object_or_404
from apps.monitoring.jmx.tasks import getJvmTriggerCounters
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    clusters = Cluster.objects.select_related().all()
    context = Context({
        'clusters': clusters,
    })
    return render(request, 'jmx.html',context)

@login_required
def node(request,node):
    # Validates if node extsts
    node = get_object_or_404(Node,name=node)
    context = Context({'node': node})
    triggers = node.cluster.triggers.all()
    for jvm in node.jvmprofiles.all():
        for trigger in triggers:
            getJvmTriggerCounters.delay(node,jvm,trigger)
    
    counterdata = []
    for trigger in triggers:
        counters = trigger.counters.all().select_subclasses()
        for counter in counters:
            if isinstance(counter, JmxCounter):
                counterdata.append(counter)
    context.update( {'counters':counterdata})
    return render(request, 'jmxnode.html',context)

@login_required
def cluster(request,cluster):
        
    # Validate if cluster extsts
    cluster = get_object_or_404(Cluster,name=cluster)
    context = Context({'cluster': cluster})
    triggers = cluster.triggers.all()
    for node in cluster.nodes.all():
        for jvm in node.jvmprofiles.all():
            for trigger in triggers:
                getJvmTriggerCounters.delay(node,jvm,trigger)
    
    counterdata = []
    for trigger in triggers:
        counters = trigger.counters.all().select_subclasses()
        for counter in counters:
            if isinstance(counter, JmxCounter):
                counterdata.append(counter)
    context.update( {'counters':counterdata})
    
    return render(request, 'jmxcluster.html',context)

@login_required
def jvm(request,node,jvm):
    """
    The **jvm** function is as an entry to the **JvmCounter** graphs pages. It uses the **jmxjvm.html** template.
    """
    node = get_object_or_404(Node,name=node)
    jvm = get_object_or_404(JvmProfile,name=jvm,node__name=node)
    context = Context({'jvm': jvm,'node': node})
    triggers = node.cluster.triggers.all()
    counterdata = []
    for trigger in triggers:
        getJvmTriggerCounters.delay(node,jvm,trigger)
        counters = trigger.counters.all().select_subclasses()
        
        for counter in counters:
            if isinstance(counter, JmxCounter):
                counterdata.append(counter)
    context.update( {'counters':counterdata})
    return render(request, 'jmxjvm.html',context)

def JmxCounterData(node,jvm,counter):
    now = datetime.datetime.now()
    utcnow = datetime.datetime.utcnow()
    #print now
    #print utcnow
    key = 'jmx_jmxcounter.' +  str(node.pk) + '.' +  str(jvm.pk) +  '.' +  str(counter.pk) + '.'
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
    for epochkey in sorted(epochkeysdict.items()):
        key = epochkey[0]
        value = epochkey[1]
        if cachedict.has_key(value):
            epochkeysdict[key]=cachedict[value]
        else:   
            epochkeysdict[key]="null"
    
    return sorted(epochkeysdict.items())

def JmxCounterData2(node,jvm,counter):
    now = datetime.datetime.now()
    utcnow = datetime.datetime.utcnow()
    #print now
    #print utcnow
    key = 'jmx_jmxcounter.' +  str(node.pk) + '.' +  str(jvm.pk) +  '.' +  str(counter.pk) + '.'
    outlist = []
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
        gckey = cache.get(ckey)
        if gckey == None:
            a=[ epoch,"null"]
        else:
            a=[ epoch,gckey]
        outlist.append(a)
    return outlist


@login_required
def clusterCounterValues(request,cluster,counter):
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
        jvmprofiles = node.jvmprofiles.all()
        for jvm in jvmprofiles:
            data = JmxCounterData(node,jvm,counter)
            data_dict = {"label":node.name + "/" + jvm.name,"data":data}
            data_out = data_out + "," + simplejson.dumps(data_dict)
    data_out = "[" + data_out[1:] + "]"
    return HttpResponse(data_out,mimetype="application/json")

@login_required
def nodeCounterValues(request,node,counter):
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
    data_out = ""
    jvmprofiles = node.jvmprofiles.all()
    for jvm in jvmprofiles:
        data = JmxCounterData(node,jvm,counter)
        data_dict = {"label":node.name + "/" + jvm.name,"data":data}
        data_out = data_out + "," + simplejson.dumps(data_dict)
    data_out = "[" + data_out[1:] + "]"
    return HttpResponse(data_out,mimetype="application/json")

@login_required
def jvmCounterValues(request,node,jvm,counter):
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
    data_out = ""
    try:
        jvm = node.jvmprofiles.get(name__exact=jvm)
    except JvmProfile.DoesNotExist:
        return HttpResponse(simplejson.dumps({}),mimetype="application/json")
    data = JmxCounterData(node,jvm,counter)
    data_dict = {"label":node.name + "/" + jvm.name,"data":data}
    data_out = "[" + simplejson.dumps(data_dict) + "]"
    return HttpResponse(data_out,mimetype="application/json")

