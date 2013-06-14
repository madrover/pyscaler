"""
The **apps.actions.models** module contains the Django models for the **actions** app.
"""
from django.db import models
from apps.control.models import Trigger,Ec2Profile,SshProfile,JvmProfile
from model_utils.managers import InheritanceManager

class Action(models.Model):
    """
    The **Action** model represents an action that can be triggered.
    This model is never accessed on its own, it is always extended by other models that implements the specific actions.
    """
    name = models.SlugField(max_length=30,unique = True)
    """
    **Action** name
    """
    triggers = models.ManyToManyField(Trigger, through='TriggerAction')
    """
    Associated **Triggers**
    """
    objects = InheritanceManager()

    def __unicode__(self):
        return unicode(self.name)
    
class TriggerAction(models.Model):
    """
    The **TriggerAction** model represents a group of **Action** that must be executed in a specific order against a specific target.
    """
    TARGET=(
                ('lastnode','LAST NODE'),
                ('cluster','CLUSTER'),
                ('none','NONE')
            )
    """
    Possible target types:

    * CLUSTER, the **Cluster** associated to the **Trigger**. Can be used by **DeployEc2Node**, **OSConfiguration**, **LocalScript** and **DistributedScript** actions.
    * LASTNODE, the last created **Node** of the **Cluster** associated to the **Trigger**. Can be used by **OSConfiguration**, **LocalScript** and **DistributedScript** actions.
    * NONE, no specified target. Can be used by **Email** action.

    """
    action = models.ForeignKey(Action,related_name='actions')
    """
    Associated **Action**.
    """
    trigger = models.ForeignKey(Trigger,related_name='triggers')
    """
    Associated **Trigger**.
    """
    target=models.CharField(max_length=20,choices=TARGET)
    """
    Target type.
    """
    order = models.IntegerField()
    
class Email(Action):
    """
    The **Email** model represents an **Action** that sends an email to the specified address.
    """
    address = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1024)

class OSConfiguration(Action):
    """
    The **OSConfiguration** model represents an Operating System configuration to be provisioned in a specific destination such as a **Node** or a **Cluster**.
    This is implemented with Puppet configuration files.
    """
    puppetfile = models.CharField(max_length=200,unique = True)
     
class LocalScript(Action):
    """
    The **LocalScript** model represents a script to be executed localy in a specific destination such as a **Node** or a **Cluster**.
    It is usually a shell script.
    """
    script = models.CharField(max_length=200,unique = True)
     
class DistributedScript(Action):
    """
    The **DistributedScript** model represents a Fabric script to be executed localy in the PyScaler server and has got a specific destination such as a **Node** or a **Cluster** as target. 
    """
    fabfile = models.CharField(max_length=200,unique = True)
    """
    Fabric's fabfile to be executed. It is execute using Fabric's **fab** utility.
    """
    commandLine  = models.CharField(max_length=255,blank=True)
    """
    Specifies additional parameters for Fabric's **fab** utility.
    """

class DeployEc2Node(Action):
    """
    The **DeployEc2Node** represents the configuration needed to deploy a new Amazon EC2 **Node**..
    """
    ec2profile = models.ForeignKey(Ec2Profile)
    """
    The **ec2profile** associated with the new **Node**.
    """
    sshprofile = models.ForeignKey(SshProfile)
    """
    The **sshprofile** associated with the new **Node**.
    """
    jvmprofile = models.ManyToManyField(JvmProfile)
    """
    The **jvmprofiles** associated with the new **Node**.
    """
    