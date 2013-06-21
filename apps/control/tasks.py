"""
The **apps.control.tasks** module contains the Celery tasks for the **control** app.
"""
from djcelery import celery
from apps.control.models import Trigger,Cluster,Node
from apps.monitoring.ssh.models import SshCounter
from apps.monitoring.jmx.models import JmxCounter
from apps.monitoring.jmx.tasks import getJvmTriggerCounters
from apps.monitoring.ssh.tasks import getSshTriggerCounters
from celery.utils.log import get_task_logger
from django.core.cache import cache

#Get celery logger
logger = get_task_logger(__name__)

@celery.task
def getTriggerCounters():
    """
    The **getTriggerCounters** task executes all the performance counter monitors defined in the **Triggers**. 
    """
#     sshcounters = SshCounter.objects.prefetch_related().all()
#     jmxcounters = JmxCounter.objects.prefetch_related().all()
    clusters = Cluster.objects.all()
    for cluster in clusters:
        triggers = cluster.triggers.all()
        nodes = cluster.nodes.all()
        for node in nodes:
            for trigger in triggers:
                launchssh = True
                launchjmx = True
                for counter in  trigger.counters.all().select_subclasses():
                    if isinstance(counter, SshCounter) and launchssh:
                        dbg = "getSshTriggerCounters " + node.name  + " " + trigger.name
                        logger.debug(dbg)
                        getSshTriggerCounters.delay(node,trigger)
                        launchssh = False

                    if isinstance(counter, JmxCounter)and launchjmx:
                        for jvm in node.jvmprofiles.all():
                            dbg = "getJvmTriggerCounters " + node.name  + " " + jvm.name  + " " + trigger.name
                            logger.debug(dbg)
                            getJvmTriggerCounters.delay(node,jvm,trigger)
                        launchjmx = False

    return "Trigger Counters Launched"


@celery.task
def checkTriggerThresholds():
    """
    The **checkTriggerThresholds** task reviews all  the **Counters** values associated with the the **Cluster** and **Triggers.
    If the **Counter** threshold has been hit more times than assigned in the **Trigger** timing value then it will execute the associated **Actions** 
    """
    
    clusters = Cluster.objects.select_related().all()
    
    # Generating dictionary with all the content needed for the template
    for cluster in clusters:
        for trigger in cluster.triggers.all():
            for counter in trigger.counters.all().select_subclasses():
                counterdict = {"cluster":cluster.name,"trigger":trigger.name,"timing":trigger.timing,"counter":counter.name,"comparison":counter.comparison,"threshold":counter.threshold,}
                launchTrigger = False
                for node in cluster.nodes.all():
                    if isinstance(counter, SshCounter):
                        key = 'ssh_sshcounter.' +  str(node.pk) + '.' +  str(counter.pk)
                        thresholdCounter = cache.get(key)
                        if thresholdCounter > trigger.timing:
                            launchTrigger = True
                        
                    if isinstance(counter, JmxCounter):
                        for jvm in node.jvmprofiles.all():
                            key = 'jmx_jmxcounter.' +  str(node.pk) + '.' +  str(jvm.pk) +  '.' +  str(counter.pk)
                            thresholdCounter = cache.get(key)
                            if thresholdCounter > trigger.timing:
                                launchTrigger = True
                    
                if launchTrigger and trigger.enabled:
                    print "Counter " + counter.name + " from Trigger " +  trigger.name + " on Cluster " + cluster.name + " has been hit " +  str(thresholdCounter) + " times. Executing associated Actions."
                    #logger.info(trigger.name + " on " + cluster.name + " has been hit " +  thresholdCounter + " times. Executing associated Actions.")
                    for node in cluster.nodes.all():
                        if isinstance(counter, SshCounter):
                            key = 'ssh_sshcounter.' +  str(node.pk) + '.' +  str(counter.pk)
                            thresholdCounter = cache.set(key,0)
                            
                        if isinstance(counter, JmxCounter):
                            for jvm in node.jvmprofiles.all():
                                key = 'jmx_jmxcounter.' +  str(node.pk) + '.' +  str(jvm.pk) +  '.' +  str(counter.pk)
                                thresholdCounter = cache.set(key,0)
