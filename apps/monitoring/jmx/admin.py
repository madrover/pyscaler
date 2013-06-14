"""
The **apps.actions.monitoring.jmx.admin** module contains the Django administration pages for the **jmx** app
"""
from django.contrib import admin
from apps.monitoring.jmx.models import JmxCounter

class JmxCounterAdmin(admin.ModelAdmin):
    """
       The **JmxCounterAdmin** class represents the **JmxCounter** model administration page  
    """
    list_display = ('name','mbean','attribute','key')
    search_fields = ('name','mbean','attribute','key')
    #list_filter = 'memberaddress_set__member__user']
    #list_filter = ['counterset_set__counter__name']
#Registering JmxCounterAdmin
admin.site.register(JmxCounter,JmxCounterAdmin)