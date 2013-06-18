Troubleshooting
======================

Pyscaler provides various logs that can help to troubleshoot the service:

- **/opt/django/pyscaler/logs/pyscaler.log**

  This log contains django's runtime log

- **/opt/django/pyscaler/logs/django_request.log**

  This log contains django requests log

- **/var/run/celery/*.log** 

  Contains the celery logs detailing the worker behavior and task status.

- **Celery flower**

  Flower is a real-time web based monitor and administration tool for Celery.
  It must be executed separated to Celery and Django and provides a deeper
  view of what is happening inside Celery

  Flower documentation can be found at `Celery's Monitoring and Management Guide <http://docs.celeryproject.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor>`_


