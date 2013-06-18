"""
This file is used by the Grappelli module and is used to configure the main dashboard of the administration pages.

"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Grappelli custom index dashboard
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        self.children.append(modules.Group(
            _('Pyscaler                                                                           '),
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    _('Control'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('apps.control.models.*',),
                ),
               modules.AppList(
                    _('Monitoring'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('apps.monitoring.*',),
                    #exclude=('django.contrib.*Group','django.contrib.*Site',),
                ),
                modules.AppList(
                    _('Actions'),
                    column=1,
                    models=('apps.actions.*',   ),
                    css_classes=('collapse closed',),
                    exclude=('django.contrib.*',),
                )
            ]
        ))
        
                             
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Django'),
            column=2,
            collapsible=True,
            children = [
                modules.AppList(
                    _('Administration'),
                    column=2,
                    collapsible=False,
                    models=('django.contrib.*','*event*'),
                    exclude=('django.contrib.*Group','django.contrib.*Site',),
                ),
                modules.AppList(
                    _('Celery'),
                    column=2,
                    css_classes=('collapse closed',),
                    models=('*celery*',),
                )
            ]
        ))
        
        # append an app list module for "Applications"
#         self.children.append(modules.AppList(
#             _('AppList: Applications'),
#             collapsible=True,
#             column=1,
#             css_classes=('collapse closed',),
#             exclude=('django.contrib.*',),
#         ))
        
        # append an app list module for "Administration"
#         self.children.append(modules.ModelList(
#             _('ModelList: Administration'),
#             column=1,
#             collapsible=False,
#             models=('django.contrib.*',),
#         ))
        
        # append another link list module for "support".

        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=3,
            children=[
                {
                    'title': _('Pyscaler Documentation'),
                    'url': 'http://pyscaler.readthedocs.org',
                    'external': True,
                },
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Celery Documentation'),
                    'url': 'http://docs.celeryproject.org/en/latest/',
                    'external': True,
                },
            ]
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


