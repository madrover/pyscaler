from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.control import tasks
from apps.control.models import Cluster
from apps.monitoring.ssh.models import SshCounter
from apps.monitoring.jmx.models import JmxCounter
from django.core.cache import cache
import datetime

@login_required
def index(request):
    """
    Shows initial monitoring page
    """
    tasks.getTriggerCounters()
    
    return render(request, 'monitoring.html')

@login_required
def triggers(request):
    """
    Shows trigger status monitoring page
    """
    counterdata=[]
    clusters = Cluster.objects.select_related().all()

    
    lasttime = datetime.datetime.now()
    lasttime = lasttime - datetime.timedelta(minutes=1)
    lasttime = lasttime.strftime('%Y%m%d%H%M')
    
    # Generating dictionary with all the content needed for the template
    for cluster in clusters:
        for trigger in cluster.triggers.all():
            for counter in trigger.counters.all().select_subclasses():
                counterdict = {"cluster":cluster.name,"trigger":trigger.name,"timing":trigger.timing,"counter":counter.name,"comparison":counter.comparison,"threshold":counter.threshold,"values":[]}
                for node in cluster.nodes.all():
                    if isinstance(counter, SshCounter):
                        key = 'ssh_sshcounter.' +  str(node.pk) + '.' +  str(counter.pk)
                        thresholdCounter = cache.get(key)
                        key = key + '.' + lasttime
                        lastvalue = cache.get(key)
                        valuedict = {"node":node.name,"lastvalue": lastvalue,"thresholdCounter": thresholdCounter}
                        counterdict["values"].append(valuedict)
                        counterdict["type"] = "SshCounter"
                        
                    if isinstance(counter, JmxCounter):
                        for jvm in node.jvmprofiles.all():
                            key = 'jmx_jmxcounter.' +  str(node.pk) + '.' +  str(jvm.pk) +  '.' +  str(counter.pk)
                            thresholdCounter = cache.get(key)
                            key = key + '.' + lasttime
                            lastvalue = cache.get(key)
                            valuedict = {"node":node.name,"jvm":jvm.name,"lastvalue": lastvalue,"thresholdCounter": thresholdCounter}
                            counterdict["values"].append(valuedict)
                            counterdict["type"] = "JmxCounter"
                counterdata.append(counterdict) 
    context = Context({
        'clusters': clusters,
        'counterdata':counterdata
    })
    tasks.checkTriggerThresholds()
    return render(request, 'triggers.html',context)



