"""
The **apps.monitoring,ssh.tasks** module contains the Celery tasks for the **ssh** app.
"""
from djcelery import celery
from django.core.cache import cache
from apps.monitoring.ssh.models import SshCounter
from celery.utils.log import get_task_logger
import datetime
import paramiko
import sys


#Get celery logger
logger = get_task_logger(__name__)

@celery.task
def getSshTriggerCounters(node,trigger):
    """
    The **getSshTriggerCounters** task connects to the **Node** parameter and executes all associated **SshCounter** from the **Trigger** parameter
    """
    logger.debug('SSH Getting ' + trigger.name + ' SshCounter counters from ' + node.name)
    output=[]
    
    #Checking if the trigger has got SshCounter
    counters = trigger.counters.all().select_subclasses()
    hascounters=False
    for counter in counters:
        if isinstance(counter, SshCounter):
            hascounters=True
    if hascounters == False:
        return 'SSH Trigger ' + trigger.name + ' does not have SshCounter counters'
    
    logger.debug('SSH Connecting to ' + node.sshprofile.user + '@' + node.hostname)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    
    try:
        mykey = paramiko.RSAKey.from_private_key_file(node.sshprofile.keyfile)
        ssh.connect(node.hostname,  username=node.sshprofile.user, pkey = mykey)
    except Exception, e:
        #Exit if we can not connect to the node via SSH
        error = 'SSH Error connecting to ' + node.hostname
        logger.error(error)
        logger.error(str(e))
        return error
    logger.debug('SSH Connected to ' + node.hostname)
    
    # Loop each trigger counter and get value from node
    for counter in counters:
        if isinstance(counter, SshCounter):
            logger.debug('SSH executing ' + counter.script)
            try:
                #channel = ssh.get_transport().open_session()
                stdin, stdout, stderr = ssh.exec_command(counter.script)
                value=''
                if stdout.channel.recv_exit_status() != 0:
                    raise Exception("Error executing "+ counter.script)
                for line in stdout:
                    value = value + line.strip('\n')
                    longkey = 'SSH ' +  node.name + ' ' +  counter.name + '  ' + datetime.datetime.now().strftime('%Y%m%d%H%M') 
                
            except Exception, e:
                error = 'SSH Error getting executing ' + counter.script + ' from Trigger "' + trigger.name + '" on ' + node.name + '. Exit status = ' + str(stdout.channel.recv_exit_status())
                logger.error(error)
                logger.error(str(e))
                ssh.close()
                return error
            
            
            key = 'ssh_sshcounter.' +  str(node.pk) + '.' +  str(counter.pk)
            # Update threshold counter in memached
            thresholdCounter = cache.get(key)
            if thresholdCounter == None:
                thresholdCounter = 0
            thresholdCounter = int(thresholdCounter)
            if counter.comparison == ">":
                if float(value) > counter.threshold:
                    thresholdCounter = thresholdCounter + 1
                else:
                    thresholdCounter = 0
            if counter.comparison == "<":
                if float(value) < counter.threshold:
                    thresholdCounter = thresholdCounter + 1
                else:
                    thresholdCounter = 0
            if counter.comparison == "=":
                if float(value) == counter.threshold:
                    thresholdCounter = thresholdCounter + 1
                else:
                    thresholdCounter = 0
            cache.set(key,thresholdCounter,86400)
            
            key = key + '.' + datetime.datetime.now().strftime('%Y%m%d%H%M') 
             
            #Send value to cache backend
            logger.debug('SSH value: ' + node.name + '.'+ counter.name + ':' + value)
            logger.debug('SSH cache entry: ' + key + ':' + value)
            cache.set(key,value,86400)
            output.append([node.name + '.' + counter.name,value])
    ssh.close()
    return output