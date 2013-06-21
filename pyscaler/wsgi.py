"""
WSGI config for pyscaler project.

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