"""
The **apps.control.tasks** module contains the Celery tasks for the **control** app.
"""
from djcelery import celery
from apps.control.models import Trigger,Cluster,Node
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
    clusters = Cluster.objects.all()
    for cluster in clusters:
        triggers = cluster.triggers.all()
        nodes = cluster.nodes.all()
        for node in nodes:
            for trigger in triggers:
                for jvm in node.jvmprofiles.all():
                    getJvmTriggerCounters.delay(node,jvm,trigger)
                getSshTriggerCounters.delay(node,trigger)
    return "getTriggerCounters OK"