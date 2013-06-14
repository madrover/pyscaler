"""
The **apps.control.models** module contains the Django models for the **control** app.
"""
from django.db import models
from apps.monitoring.models import Counter

class JvmProfile(models.Model):
    """
    The **JVMProfile** model represents the configuration needed to connect to a remote JVM via JMX.
    """
    name = models.SlugField(max_length=30,unique = True)
    """
    **JvmProfile** name.
    """
    port = models.IntegerField()
    """
    JMX port.
    """
    user = models.CharField(max_length=30, default="",blank=True)
    """
    JMX user.
    """
    password = models.CharField(max_length=30, default="",blank=True)
    """
    JMX password.
    """
    def __unicode__(self):
        return unicode(self.name)
    
class SshProfile(models.Model):
    """
    The **SshProfile** model represents the configuration needed to connect to **Node** via SSH.
    """
    name = models.SlugField(max_length=30,unique = True)
    """
    **SshProfile** name.
    """
    user = models.CharField(max_length=30, default="",blank=True)
    """
    User name to connect via SSH.
    """
    keyfile = models.CharField(max_length=256, default="",blank=True)
    """
    Private key file path used for key authentication.
    """
    def __unicode__(self):
        return unicode(self.name)
    
class Ec2Profile(models.Model):
    """
    The **Ec2Profile** class represents the EC2 configuration associated with a **Node**
    """
    INSTANCE_TYPE=(
                ('t1.micro', 't1.micro'),
                ('m1.small', 'm1.smal'),
                ('m1.medium', 'm1.medium'),
                ('m1.large', 'm1.xlarge'),
                ('m1.xlarge', 'm1.xlarge'),
                ('m3.xlarge', 'm3.xlarge'),
                ('m3.2xlarge', 'm3.2xlarge'),
                ('c1.medium', 'c1.medium'),
                ('c1.xlarge', 'c1.xlarge'),
                ('m2.xlarge', 'c1.xlarge'),
                ('m2.2xlarge', 'm2.2xlarge'),
                ('m2.4xlarge', 'm2.2xlarge'),
                ('cr1.8xlarge', 'cr1.8xlarge'),
                ('hi1.4xlarge', 'hi1.4xlarge'),
                ('hs1.8xlarge', 'hs1.8xlarge'),
                ('cc1.4xlarge', 'cc1.4xlarge'),
                ('cg1.4xlarge', 'cg1.4xlarge'),
                ('cc2.8xlarge', 'cc2.8xlarge')
            )
    """
    Available EC2 instance types.
    """
    REGION=(
                ('us-east-1','US East (N. Virginia)'),
                ('us-west-2','US West (Oregon)'),
                ('us-west-1','US West (N. California)'),
                ('eu-west-1','EU (Ireland)'),
                ('ap-southeast-1','Asia Pacific (Singapore)'),
                ('ap-northeast-1','Asia Pacific (Tokyo)'),
                ('ap-southeast-2','Asia Pacific (Sydney)'),
                ('sa-east-1','South America (Sao Paulo)')
            )
    """
    Avaliable regions for Ec2 instances
    """
    name = models.SlugField(max_length=30,unique = True)
    """
    **Ec2Profile** name
    """
    key_name=models.CharField(max_length=100)
    """
    Ec2 instance ssh key pair
    """
    instance_type=models.CharField(max_length=20,choices=INSTANCE_TYPE)
    """
    Ec2 instance type
    """
    security_groups=models.CharField(max_length=200,blank=True)
    """
    Ec2 firewall security group
    """
    user_data=models.CharField(max_length=512,blank=True)
    """
    Ec2 instance custom user_data field
    """
    region=models.CharField(max_length=20,choices=REGION)
    """
    Ec2 instance region
    """
    load_balancer=models.CharField(max_length=100,blank=True)
    """
    Associated Elastic Load Balancer instance
    """
    image_id=models.CharField(max_length=20)
    """
    Ec2 instance AMI
    """
    def __unicode__(self):
        return unicode(self.name)
    
#The Cluster model is a group of servers
class Cluster(models.Model):
    name = models.SlugField(max_length=30,unique = True)
    """
    **Cluster** name
    """
    def __unicode__(self):
        return unicode(self.name)
    
#The Node model is a representation of a host, a single computer either phyisical or VM  
class Node(models.Model):
    name = models.SlugField(max_length=30,unique = True)
    """
    **Node** name
    """
    hostname = models.CharField(max_length=100)
    """
    **Node** dns name or ip address
    """
    cluster = models.ForeignKey(Cluster,related_name='nodes')
    """
    Associated **Cluster**
    """
    ec2profile = models.ForeignKey(Ec2Profile)
    """
    Associated **Ec2Profile**
    """
    sshprofile = models.ForeignKey(SshProfile)
    """
    Associated **SshProfile**
    """
    jvmprofiles = models.ManyToManyField(JvmProfile,blank=True,null=True)
    """
    Associated **JvmProfiles**.
    """
    def __unicode__(self):
        return unicode(self.name)

class Trigger(models.Model):
    name = models.SlugField(max_length=30,unique = True)
    """
    **Trigger** name.
    """
    counters = models.ManyToManyField(Counter,related_name='triggers')
    """
    Associated **Counters**.
    """
    timing = models.IntegerField()
    """
    Number of minutes that must elapse when any of the associated thresholds are reached until the associated **Actions** are executed.
    """
    cluster = models.ForeignKey(Cluster,related_name='triggers')
    """
    Associated **Cluster**
    """
    enabled = models.BooleanField(default=True)
    """
    **Trigger** enabled or not.
    """
    def __unicode__(self):
        return unicode(self.name)