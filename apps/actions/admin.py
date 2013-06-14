"""
The **apps.actions.admin** module contains the Django administration pages for the **actions** app
"""
from django.contrib import admin
from apps.actions.models import OSConfiguration, LocalScript, DistributedScript,Email,DeployEc2Node

class OSConfigurationAdmin(admin.ModelAdmin):
    """
    The OSConfigurationAdmin class represents the OSConfiguration model administration page 
    """
    list_display = ('name',)
    search_fields = ('name',)
#Registering OSConfigurationAdmin
admin.site.register(OSConfiguration,OSConfigurationAdmin)

class LocalScriptAdmin(admin.ModelAdmin):
    """
    The **LocalScriptAdmin** class represents the **LocalScript** model administration page 
    """
    list_display = ('name',)
    search_fields = ('name',)
#Registering LocalScriptAdmin
admin.site.register(LocalScript,LocalScriptAdmin)

class DistributedScriptAdmin(admin.ModelAdmin):
    """
    The **DistributedScriptAdmin** class represents the **DistributedScript** model administration page 
    """
    list_display = ('name','commandLine',)
    search_fields = ('name','commandLine,')
#Registering DistributedScriptAdmin
admin.site.register(DistributedScript,DistributedScriptAdmin)

class EmailAdmin(admin.ModelAdmin):
    """
    The **EmailAdmin** class represents the **Email** model administration page 
    """
    list_display = ('name','address','title','content')
    search_fields = ('name','address','title','content')
#Registering EmailAdmin
admin.site.register(Email,EmailAdmin)

class DeployEc2ProfileAdmin(admin.ModelAdmin):
    """
    The **DeployEc2ProfileAdmin** class represents the **DeployEc2Profile** model administration page 
    """
    list_display = ('name','ec2profile','sshprofile',)
    search_fields = ('name','ec2profile','sshprofile',)
    filter_horizontal = ('jvmprofile',)
#Registering DeployEc2ProfileAdmin
admin.site.register(DeployEc2Node,DeployEc2ProfileAdmin)