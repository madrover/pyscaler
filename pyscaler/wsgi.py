"""
WSGI config for pyscaler project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""


# http://technomilk.wordpress.com/2011/08/10/running-our-django-site-with-mod_wsgi-and-virtualenv-part-2/

import os
import sys
import site

# set up python path and virtualenv
site.addsitedir('/home/pyscaler/.virtualenv/pyscaler/lib/python2.6/site-packages')
sys.path.append('/opt/django/pyscaler/')
                
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyscaler.settings")

import pyscaler.startup as startup
startup.run()

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)