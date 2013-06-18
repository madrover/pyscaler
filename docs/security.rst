Security
===========

This section describes the main security related points of PyScaler

Django authentication 
---------------------------------
Being PyScaler a Django based application it delegates the security to Django's
security mechanisms.

All urls are protected except the homepage. If an user tries to access a secured page 
without being logged it will be automatically redirected to a login page.

Users can be managed from the administration pages.

Django protection
-------------------------
Django provides the following protection mechanisms againts possible attackers:

- Cross site scripting (XSS) protection
- Cross site request forgery (CSRF) protection
- SQL injection protection
- SSL/HTTPS

Key based ssh
------------------------------

All SSH communications must be authenticatd using key files. The usage of key files 
provides a higher level of control and enables easier automation.

Authenticated JMX
-----------------------------------

JMX connection to JVM can be secured using user and password

Key based AWS authentication
---------------------------------------------

All communications agains Amazon Web Services are authenticad using a public key authentication.