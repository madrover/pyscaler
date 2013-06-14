"""
The **apps.monitoring,jmx.tasks** module contains the Celery tasks for the **jmx** app.
"""
import jpype
from jpype import java
from jpype import javax
from djcelery import celery
from django.core.cache import cache
from apps.monitoring.jmx.models import JmxCounter
from celery.utils.log import get_task_logger
import datetime
import inspect

#Get celery logger
logger = get_task_logger(__name__)

@celery.task
def getJvmTriggerCounters(node,jvm,trigger):
    """
    The **getJvmTriggerCounters** task connects to the **JVM** in **Node** and executes all associated **JmxCounter** from the **Trigger** parameter
    """

    logger.debug('JMX Getting ' + trigger.name + ' JmxCounter counters from ' + node.name)
    
    #Checking if the trigger has got JmxCounter
    counters = trigger.counters.all().select_subclasses()
    hascounters=False
    for counter in counters:
        if isinstance(counter, JmxCounter):
            hascounters=True
    if hascounters == False:
        error = 'JMX Trigger ' + trigger.name + ' does not have JmxCounter counters'
        logger.debug(error)
        return error
    
    output = []
    #Checking if JVM is loaded and load if not
    if not jpype.isJVMStarted():
        jpype.startJVM(jpype.getDefaultJVMPath())
    #Checking if JVM is attached to the current thread and attach if not
    if not jpype.isThreadAttachedToJVM():
        jpype.attachThreadToJVM()
    
    URL = 'service:jmx:rmi:///jndi/rmi://%s:%d/jmxrmi' % (node.hostname, jvm.port)
    
    #Building JMX url
    jhash = java.util.HashMap()
    if jvm.user != '':
        jarray=jpype.JArray(java.lang.String)([jvm.user,jvm.password])
        jhash.put (javax.management.remote.JMXConnector.CREDENTIALS, jarray);
    jmxurl = javax.management.remote.JMXServiceURL(URL)
    #Connecting to JMX url
    logger.debug('JMX Connecting to ' + URL)
    try:
        jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl,jhash)
        connection = jmxsoc.getMBeanServerConnection();
    except Exception, e:
        #Exit if we can not connect to the JMX url
        error = 'JMX Error connecting to ' + URL
        logger.error(error)
        logger.error(str(e))
        return error
    logger.debug('JMX Connected to ' + URL)
    

    # Loop each trigger counter and get value from JVM
    for counter in trigger.counters.all().select_subclasses():
        if isinstance(counter, JmxCounter):
            logger.debug('JMX Getting ' + counter.mbean)
            try:
                attr=connection.getAttribute(javax.management.ObjectName(counter.mbean),counter.attribute)
                if counter.key == '':
                    value = str(attr)
                else:
                    value =  str(attr.contents.get(counter.key))
                #logger.info(longkey + ':' + value)
                
            except Exception, e:
                error = 'JMX Error getting mbean ' + counter.mbean + ' on ' + jvm.name + ' from ' + node.name
                logger.error(error)
                logger.error(str(e))
                return error
            key = 'jmx_jmxcounter.' +  str(node.pk) + '.' +  str(jvm.pk) +  '.' +  str(counter.pk) + '.' + datetime.datetime.now().strftime('%Y%m%d%H%M') 
            #Send value to cache backend
            logger.debug('JMX value: ' + node.name + '.' + jvm.name + '.' + counter.name + ':' + value)
            logger.debug('JMX cache entry: ' + key + ':' + value)
            cache.set(key,value,86400)
            output.append([node.name + '.' + jvm.name + '.' + counter.name,value])
    jmxsoc.close()
    return output