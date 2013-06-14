"""
The **apps.actions.tasks** module contains the Celery tasks for the **actions** app.
"""
from djcelery import celery
from celery.utils.log import get_task_logger
import time
from apps.actions.models import DistributedScript, LocalScript
from apps.control.models import Cluster, Node
import subprocess
from django.conf import settings
import boto, boto.ec2

#Get celery logger
logger = get_task_logger(__name__)


@celery.task
def executeScript(destination,script):
    """
    | The **executeScript** task executes **LocalScripts** or **DistributedScripts** using Fabric's **fab** utility.   
    | It can be used using both **Nodes** or **Clusters** as destinations    
    | If the script is a **LocalScript** then **fab** will run the an operating system script locally on each destination    
    | If the script is a **DistributedScript** then **fab** will run a Fabric's fabfile locally on the PyScaler service but using the defined destination as target   
    
    """
    hosts = ""
    keyfiles = ""
    #Check destination type and prepare fab parameters depending on it
    if isinstance(destination, Node):
        hosts = destination.sshprofile.user + "@" + destination.hostname
        keyfiles = " -i " + destination.sshprofile.keyfile
    elif isinstance(destination, Cluster):
        for node in destination.nodes.all():
            host = node.sshprofile.user + "@" + node.hostname
            hosts = hosts + "," + host
            keyfiles = keyfiles + " -i " + node.sshprofile.keyfile
        hosts = hosts[1:]
               
    args = "fab --abort-on-prompts -H " + hosts + keyfiles
    
    #Preparing fab parameters
    if isinstance(script, LocalScript):
        args = args + " -- " + script.script
    elif isinstance(script, DistributedScript):
        args = args + " -f " + script.fabfile +  " " + script.commandLine

    #Executing fab
    try:
        p = subprocess.Popen(args, stdout=subprocess.PIPE,stderr =subprocess.STDOUT, shell=True)
        (out, err) = p.communicate()
    except Exception, e:
        logger.error("Error executing fab")
        raise e 

    return out


@celery.task
def ec2nodeDeploy(cluster,ec2profile,sshprofile,jvmprofiles):
    """
    | The **ec2nodeDeploy** launches an ec2 instance using a Ec2Node as template and adds it to the specifed Cluster.    
    | It needs **AWSAccessKeyId** and **AWSSecretKey** to be defined in Django's **settings.py**
    """
    
    logger.debug("Determining new node name")
    nodes = []
    for node in cluster.nodes.all():
        nodes.append(node.name)
    nodename = ""
    for i in range(1,100):
        nodename = cluster.name + str(i).rjust(2,"0")
        if nodename not in nodes:
            break

    logger.debug("Connecting to AWS")
    try:
        conn = boto.ec2.connect_to_region(ec2profile.region,
                                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    except Exception as e:
        result="ERROR\n" + str(e)
        return result
    
    logger.debug("Creating new EC2 instance for node " + nodename)
    try:
        reservation = conn.run_instances(
            image_id = ec2profile.image_id ,
            key_name=ec2profile.key_name,
            instance_type=ec2profile.instance_type,
            security_groups=[ec2profile.security_groups],
            user_data=ec2profile.user_data)
    except Exception as e:
        result="ERROR\n" + str(e)
        return result
    
    instance = reservation.instances[0]
    # Check up on its status every so often
    status = instance.update()
    while status == 'pending':
        time.sleep(10)
        status = instance.update()
    # Add instance tags when deployed
    if status == 'running':
        instance.add_tag("Name",nodename)
        instance.add_tag("Cluster",cluster.name)
    else:
        result='Instance status: ' + status
        return result
    
    #Creating new Node inside PyScaler
    try:
        node = Node(name=nodename,cluster=cluster,ec2profile= ec2profile, hostname=instance.public_dns_name,sshprofile=sshprofile)
        node.save()
        for jvmprofile in jvmprofiles:
            node.jvmprofiles.add(jvmprofile)
        node.save()
    except Exception as e:
        result="ERROR\n" + str(e)
        return result
    
    result = "New node " + nodename + " on cluster " + cluster.name + " with hostname " + instance.public_dns_name

    return result

@celery.task
def ec2nodeRemove(cluster,node):
    """
    | The **ec2nodeRemove** task removes a **Node** and its associated ec2 instance.
    | It needs **AWSAccessKeyId** and **AWSSecretKey** to be defined in Django's **settings.py**
    """
    if not isinstance(cluster, Cluster):
        cluster = Cluster.objects.get(name=cluster)
    if not isinstance(node, Node):
        node = Node.objects.get(name=node, cluster__name=cluster.name)
        
        
    conn = boto.ec2.connect_to_region(node.ec2profile.region,
                                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]

    output = ""
    for instance in instances:
        tags = instance.__dict__['tags']
        if "Name" in tags and "Cluster" in tags:
            if tags['Name'] == node.name and tags['Cluster'] == cluster.name:
                instanceid =  instance.__dict__['id']
                if instance.state == "running":  
                    conn.terminate_instances(instance_ids=[instanceid])
                    output = "Node " + node.name + " from cluster " + cluster.name + " deleted."
                    node.delete()
    return output
