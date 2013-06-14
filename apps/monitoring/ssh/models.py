"""
The **apps.monitoring.ssh.models** module contains the Django models for the **ssh** app.
"""
from django.db import models
from apps.monitoring.models import Counter
from apps.control.models import Node

class SshCounter(Counter):
    """
    The **SshCounter*** model implements a **Counter** and reprents a script to be execute via SSH on a remote destination and returns a single numeric value
    """
    script = models.CharField(max_length=250)
    #counterset = models.ManyToManyField(CounterSet, through='SshThreshold',related_name="%(app_label)s_%(class)s_related")
