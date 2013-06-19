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

    return "getTriggerCounters OK"