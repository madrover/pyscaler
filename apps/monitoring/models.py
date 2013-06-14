"""
This file contains the model definitions for the **apps.monitorings** module
"""
from django.db import models
from django.db.models import get_model
from model_utils.managers import InheritanceManager

 
class Counter(models.Model):
    """
    Generic class that represents a peformance counter to be monitored.
    Will be extended by the different types of Target
    """
    name = models.SlugField(max_length=100,unique = True)
     
    COMPARISON = (
        ('<', 'Smaller'),
        ('=', 'Equal'),
        ('>', 'Greater'),
    )
    comparison = models.CharField(max_length=1, choices=COMPARISON)
    threshold = models.CharField(max_length=30)
    objects = InheritanceManager()
    def __unicode__(self):
        return unicode(self.name)
#     class Meta:
#         abstract = True
