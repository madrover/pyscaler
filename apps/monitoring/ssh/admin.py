"""
The **apps.actions.monitoring.ssh.admin** module contains the Django administration pages for the **ssh** app
"""
from django.contrib import admin
from apps.monitoring.ssh.models import SshCounter

# class SshAdmin(admin.ModelAdmin):
#     list_display = ('name', 'node','user')
#     search_fields = ('name', 'user')
#     list_filter = ( 'node',)
# admin.site.register(Ssh,SshAdmin)

class SshCounterAdmin(admin.ModelAdmin):
    """
    The **SshCounterAdmin** class represents the **SshCounter** model administration page 
    """
    list_display = ('name','script')
    search_fields = ('name','script')
    #list_filter = 'memberaddress_set__member__user']
    #list_filter = ['counterset_set__counter__name']
#Registering SshCounterAdmin
admin.site.register(SshCounter,SshCounterAdmin)