"""
The **apps.actions.control.admin** module contains the Django administration pages for the **control** app
"""
from django.contrib import admin
from apps.control.models import Node,Cluster,Trigger,JvmProfile,SshProfile,Ec2Profile
from apps.actions.models import TriggerAction


class JvmProfileAdmin(admin.ModelAdmin):
    """
    The **JvmProfileAdmin** class represents the **JvmProfile** model administration page 
    """
    list_display = ('name','port','user')
    search_fields = ('name','port','user')
    list_filter = ('name','port','user')
#Registering JVMAdmin
admin.site.register(JvmProfile,JvmProfileAdmin)

class SshProfileAdmin(admin.ModelAdmin):
    """
    The **SshProfileAdmin** class represents the **SshProfile** model administration page
    """
    model = SshProfile
    fields = ('name','user', 'keyfile')
    list_display = ('name','user', 'keyfile')
    search_fields = ('name','user', 'keyfile')
admin.site.register(SshProfile,SshProfileAdmin)

class Ec2ProfileAdmin(admin.ModelAdmin):
    """
    The **Ec2ProfileAdmin** class represents the **Ec2Profile** model administration page
    """
    model = Ec2Profile
    fields = ('name','image_id','key_name','instance_type','security_groups','user_data','region','load_balancer')
    list_display = ('name','image_id','key_name','instance_type','security_groups','user_data','region','load_balancer')
    search_fields = ('name','image_id','key_name','instance_type','security_groups','user_data','region','load_balancer')
admin.site.register(Ec2Profile,Ec2ProfileAdmin)

class NodeAdmin(admin.ModelAdmin):
    """
    The **NodeAdmin** class represents the **Node** model administration page 
    """
    model = Node
    list_display = ('name','hostname','ec2profile','sshprofile')
    search_fields = ('name','hostname','ec2profile','sshprofile')
    filter_horizontal = ('jvmprofiles',)
#Registering NodeAdmin
admin.site.register(Node,NodeAdmin)

class NodeInline(admin.StackedInline):
    """
    The **NodeInline** class represents a **Node** model inline form to be embedded into the **ClusterAdmin** administration page
    """
    model = Node
    can_delete = False
    filter_horizontal = ('jvmprofiles',)

class TriggerInline(admin.StackedInline):
    """
    The **TriggerInline** class represents a **Trigger** model inline form to be embedded into the **ClusterAdmin** administration page
    """
    model = Trigger
    can_delete = False
    filter_horizontal = ('counters',)

class ClusterAdmin(admin.ModelAdmin):
    """
    The **ClusterAdmin** class represents the **Cluster** model administration page 
    """
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [
        NodeInline,
        TriggerInline,
    ]
#Registering ClusterAdmin
admin.site.register(Cluster,ClusterAdmin)

class TriggerActionInline(admin.TabularInline):
    """
    The **TriggerActionInline** class represents a **TriggerAction** model inline form to be embedded into the **TriggerAdmin** administration page
    """
    model = TriggerAction
    extra = 1
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('order', 'action','target')
        }),
    )
    
class TriggerAdmin(admin.ModelAdmin):
    """
    The **TriggerAdmin** class represents the **Trigger** model administration page 
    """
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [
        TriggerActionInline,
    ]
    filter_horizontal = ('counters',)
#Registering TriggerAdmin
admin.site.register(Trigger,TriggerAdmin)
