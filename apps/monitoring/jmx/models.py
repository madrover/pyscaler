"""
The **apps.monitoring.jmx.models** module contains the Django models for the **jmx** app.
"""
from django.db import models
from apps.monitoring.models import  Counter
from apps.control.models import Node


class JmxCounter(Counter):
    """
    The **JmxCounter** class implements a **Counter** class and represents the Mbean path and detaiils needed to gather JVM infomation via JMX.
    It returns a single numeric value
    """
    mbean = models.CharField(max_length=250)
    attribute = models.CharField(max_length=100)
    key = models.CharField(max_length=50,default="",blank=True)
    #counterset = models.ManyToManyField(CounterSet, through='JmxThreshold',related_name="%(app_label)s_%(class)s_related")   