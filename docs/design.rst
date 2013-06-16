Design
========

Concepts
-----------

- **Node** Virtual machines running applications
- **Cluster** Group of Nodes executing the same applications and work
   together
- **Counter** Performance counter to be gathered. It can be a JMX counter
  on a JVM or an operating system script to be executed via SSH. It has 
  got a Threshold field.

.. figure:: images/Data-Model.png
   :align: center
   :alt: 

- **Trigger** Group of Counters associated to a Cluster. It has got a Timing 
  field and a list of associated and ordered Actions. When any of the associated
  Counters reaches its threshold during the number of minutes defined in the
  Timing field it will execute the associated Actions

- **Action** Actions that can be executed against Nodes or Clusters. They can be
  for management tasks or to deploy new Nodes if needed. The following actions 
  are available:

 - **DeployEc2Node** Deploy a new virtual machine on EC2 and create a new Node
 - **DistributedScript** Execute a Fabric script
 - **Email** Send an email
 - **LocalScript** Execute a local command in the target (i.e. shell script)
 - **RemoveEc2Node** Stops a virtual machine on EC2 and removes its associated Node
 - **OSConfiguration** Enforce an operating system configuration via Puppet

PyScaler main components
---------------------------

.. figure:: images/Components.png
   :align: center
   :alt: 

Django
~~~~~~~~

`https://www.djangoproject.com/ <https://www.djangoproject.com/>`_

PyScaler is essentially a python web application based on the Django
framework.

The core Django
`MVC <http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ framework
consists of an `object-relational
mapper <http://en.wikipedia.org/wiki/Object-relational_mapping>`_ which
mediates between `data
models <http://en.wikipedia.org/wiki/Data_modeling>`_ (defined as Python
classes) and a `relational
database <http://en.wikipedia.org/wiki/Relational_database>`_ ("Model");
a system for processing requests with a `web templating
system <http://en.wikipedia.org/wiki/Web_template_system>`_ ("View") and
a
`regular-expression <http://en.wikipedia.org/wiki/Regular_expression>`_-based
`URL <http://en.wikipedia.org/wiki/Uniform_Resource_Locator>`_ dispatcher
("Controller").

Django applications are structured in project and apps. A Django project
is a collection of settings for an instance of Django, including
database configuration, Django-specific options and application-specific
settings. A Django app is a bundle of Django code, including models and
views, that lives together in a single Python package and represents a
full Django application.

Django provides a Object-relational Mapping (ORM, O/RM, and O/R mapping)
layer that provides an abstraction layer to the underlying database
backend. Instead of defining database tables, indexes, relationships,
etc..., you define Django models that represent the application data
layout. Django ORM supports many different database backends as SQLite,
MySql, etc...

Celery
~~~~~~~~~

`http://www.celeryproject.org/ <http://www.celeryproject.org/>`_

Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

Some common Celery use cases:

#. Running something in the background. For example, to finish the web
   request as soon as possible, then update the users page
   incrementally.
#. Running something after the web request has finished.
#. Making sure something is done, by executing it asynchronously and
   using retries.
#. Scheduling periodic work.

As Django is a web application it just executes code when an url is
called. As PyScaler needs to execute code on a scheduled basis
(performance data collecting, etc...), it relies on Celery scheduling
capabilities to automate the code execution.

PyScaler can invoke lengthy operations such as virtual machine
deployments, etc... Being PyScaler a web application it is supposed to
be responsive and it can not wait a for this lengthy operations to be
finished. PyScaler overcome this situation by packaging these lengthy
tasks into asynchronous celery task that are executed in the background.

SQLite
~~~~~~~~
`http://www.sqlite.org/ <http://www.sqlite.org/>`_

SQLite is a self-contained, serverless, zero-configuration,
transactional SQL database engine.

Using the

Memcached
~~~~~~~~~~~~~~~~~~~~~~

RabbitMQ
~~~~~~~~~~~~~~~~~~~~~~

Gnunicorn
~~~~~~~~~~~~~~~~~~~~~~

Nginx
~~~~~~~~~~~~~~~~~~~~~~

Puppet
~~~~~~~~~~~~~~~~~~~~~~

Amazon AWS
~~~~~~~~~~~~~~~~~~~~~~



Project layout
------------------------------------------

As we have stated before a Django based application has got a project
and different apps. The following section describes how the the project
is organized.

PyScaler project
~~~~~~~~~~~~~~~~~~~~~~

The top-level folder contains:

+-- apps Folder containing the Django apps  
+-- docs Folder containing documentation in reStructuredText format  
+-- fixtures Folder containing json files with the initial database data  
+-- logs Folder containing Django logs
+-- manage.py Script used to manage the Django site.
+-- pyscaler Folder containing the Django project
¦   +-- dashboard.py File containing administration pages configuration
¦   +-- \_\_init\_\_.py File that tells Python that this directory is a Python module
¦   +-- receivers.py File containing Django signal receiver functions
¦   +-- settings.py File containing all of the Django project settings
¦   +-- site\_media Folder containing statics assets of the project
¦   +-- startup.py File containing code to be loaded at startup
¦   +-- static Folder containing statics assets of installed applications
¦   +-- templates Folder containing html templates to be used project wide
¦   +-- urls.py File containing  the project root URL configuration
¦   +-- views.py File containing  the project root views
¦   +-- wsgi.py File containing the WSGI application configuration
+-- requirements.txt File containing the library requirements for the project


Monitoring App
~~~~~~~~~~~~~~~~~~~~~~

DESCRIPTION
^^^^^^^^^^^^

This app is responsible of connecting to remote servers and collect
performance data. It has got different sub apps for each different
possible performance data sources. The currently implemented performance
datasources are SSH and JMX

This app outputs the collected performance data the collected
performance counters to filesystem log and to the shared cache
(memcached)

This app is defined in the django app apps.monitoring

Views
^^^^^^^^^^^^^^^

These are the views and urls provided by the apps.monitoring app

#. http://pyscaler/monitoring/

This view lists the available clusters and nodes and provides access to
them

#. http://pyscaler/monitoring/cluster/<CLUSTER>

This view shows aggregate graphs for the available performance counters
in all the cluster nodes. It takes last element of the URL as the
requested cluster name.

#. http://pyscaler/monitoring/node/<NODE>

This view shows aggregate graphs for the available performance counters
in a specific node. It takes last element of the URL as the requested
node name.

Tasks
^^^^^^^^^^^^^^^

These are the Celery tasks provided by the apps.monitoring app

#. launchTriggers

This is a scheduled task that executes every minute and tries to collect
all the counters defined in the triggers.


JMX Monitoring App
------------------------------------------------------

This app is used to connect to JVM instances with JMX enabled and
collect performance data. This app is defined in the django
package apps.monitoring.jmx

Tasks
~~~~~~~~~

#. getJvmTriggerValues(jvm,trigger)

This tasks connects to the specified JVM and collects all the JMX
counters defined in the trigger.

Views
~~~~~~~~~

#. http://pyscaler/monitoring/jmx/

This view contains links to the configured available clusters, nodes and
JVMs

2. http://pyscaler/monitoring/jmx/cluster/<CLUSTER>

This view shows aggregate graphs for the available JMX counters in all
the cluster nodes. It takes last element of the URL as the requested
cluster name. The graph data is consumed via JSON webservice.

2. http://pyscaler/monitoring/jmx/node/<NODE>

This view shows aggregate graphs for the available JMX counters in a
specific node. It takes last element of the URL as the requested node
name. The graph data is consumed via JSON webservice.

3. http://pyscaler/monitoring/jmx/jvm/<NODE>/<JVM>

This view shows aggregate graphs for the available JMX counters in a
specific node. It takes last element of the URL as the requested node
name. The graph data is consumed via JSON webservice.

3. http://pyscaler/monitoring/jmx/json/cluster/<CLUSTER>/<COUNTER>

This view returns the last 24h values of a specific counter in all
cluster JVMs in JSON format. It takes last element of the URL as the
requested counter name and the previous element as the requested cluster
name.

4. http://pyscaler/monitoring/jmx/json/node/<NODE>/<COUNTER>

This view returns the last 24h values of a specific counter in all node
JVMs in JSON format. It takes last element of the URL as the requested
counter name and the previous element as the requested node name.

5. http://pyscaler/monitoring/jmx/json/jvm/<NODE>/<JVM>/<COUNTER>

This view returns the last 24h values of a specific counter in a
specific JVMs in JSON format. It takes last element of the URL as the
requested counter name, the previous element as the requested JVM name
and the previous as the requested node name.

Libraries
~~~~~~~~~

#. Jpype `http://jpype.sourceforge.net/ <http://jpype.sourceforge.net/>`_

This library is used to execute java classes from python scripts. It is
used in the project to execute JMX related code to collect remote JVMs
performance data.


SSH monitoring app
------------------

This app is used to connect via ssh to hosts and execute a script. The
output of this script must be an integer value that represents a
performance counter. This app is defined in the django
package apps.monitoring.ssh

Tasks
~~~~~~~~~

2. getSshTriggerValues(ssh,trigger)

This tasks connects to the specified ssh node and executes the scripts
defined in the trigger. It stores the output data in Memcache.

Views
~~~~~~~~~

6. http://pyscaler/monitoring/ssh/

This view contains links to the configured available clusters and nodes.

4. http://pyscaler/monitoring/ssh/cluster/<CLUSTER>

This view shows aggregate graphs for the available ssh counters in all
the cluster nodes. It takes last element of the URL as the requested
cluster name.

7. http://pyscaler/monitoring/ssh/node/<NODE>

This view shows aggregate graphs for the available ssh counters in a
specific node. It takes last element of the URL as the requested node
name.

5. http://pyscaler/monitoring/ssh/json/cluster/<CLUSTER>/<COUNTER>

This view returns the last 24h values of a specific counter in all
cluster nodes in JSON format. It takes last element of the URL as the
requested counter name and the previous element as the requested cluster
name.

8. http://pyscaler/monitoring/ssh/json/node/<NODE>/<COUNTER>

This view returns the last 24h values of a specific counter in a node in
JSON format. It takes last element of the URL as the requested counter
name and the previous element as the requested node name.

Libraries
~~~~~~~~~

2. Paramiko `https://github.com/paramiko/paramiko <https://github.com/paramiko/paramiko>`_

This library is used to execute scripts in remote hosts via SSH from
python.



Control module
--------------

This modules contains the business logic of the application. It has the
following roles:

#. Manages Cluster and Nodes objects. Can add and remove Nodes
   definitions and handles the Cluster integration
#. Triggers the Counters defined in the Clusters’ Triggers
#. Triggers groups of actions, either manually or due a Trigger
   threshold

This module is defined in the django app apps.control

Tasks
~~~~~~~~~

3. launchTriggers()

Analyzes all Clusters’ Triggers and execute associated Target’s Counters
to gather performance data. This task is scheduled to be executed every
minute.

#. analyzePerfomanceData()

Analyzes the performance data in the backend and triggers the ActionSets
defined in the Triggerss if the associated counters hit their Thresholds
during a specified amount of time.

Views
~~~~~~~~~

9. http://pyscaler/control/

This view contains links to the configured available Cluster and Nodes

6. http://pyscaler/control/cluster/<CLUSTER>

This view can execute Actions on a Node

#. http://pyscaler/control/node/<NODE>

This view can execute Actions on a Node

#. http://pyscaler/control/cluster/<CLUSTER>/execute/<ACTION>

This view executes the specified action on the specified cluster and
returns a Celery Task ID

2. http://pyscaler/control/node/<NODE>/execute/<ACTION>
3. http://pyscaler/control/execute/status/<TASKID>
4. http://pyscaler/control/execute/output/<TASKID>


Tasks
~~~~~~~~~

10. email

It implements and Action that sends an email to a specific email
address.

Actions module
------------------------------------------

This module is used to deploy new nodes to a cluster. It interacts with
the virtual machine provider and deploys new servers.

Tasks
~~~~~~~~~

11. OperatingSystemConfiguration()

It implements and Action that enforces a Puppet manifest into a specific
Node

12. Ec2VMDeploy

It implements and Action that deploys a new VM to EC2

#. ApplicationConfiguration()

It implements and Action that executes a Fabric fabfile against a
specific Node

Libraries
~~~~~~~~~

#. Boto A Python package that provides interfaces to Amazon Web
   Services. It is used to deploy new virtual machines on EC2
#. Fabric A Python (2.5 or higher) library and command-line tool for
   streamlining the use of SSH for application deployment or systems
   administration tasks.

  

Data Model
------------------------------------------

There are two types of data managed by

Performance data
------------------------------------------------

The performance data is stored in Memcached.

Key / Value format

jmx\_jmxcounter.<nodeId>.<jvmid>.<counterid>.yymmhhddhhmmss : <Value>

ssh\_sshcounter.<nodeId>.<jvmid>.<counterid>.yymmhhddhhmmss : <Value>

Configuration data
--------------------------------------------------

Django provides an
`Object-relational\_mapping <http://en.wikipedia.org/wiki/Object-relational_mapping>`_\ layer
that avoids the need of designing the database layout.

With django you define your data structure by using model classes. A
model is the single, definitive source of data about your data. It
contains the essential fields and behaviors of the data you’re storing.
Generally, each model maps to a single database table. Each module has
got different models that are interconnected between them.

The following models contains the configuration information of PyScaler

----------------------------------------------

Configuration data models
---------------------------------------------------------

.. figure:: images/Cluster-Node-Counter.png
   :align: center
   :alt: 

New Virtual Machine deployment steps

ActionSet has configuration

baseNodeName, will increment

baseJVMName, will increment

JVMNumber, will increment

- Deploy a new VM on EC2 (clustername,user, )

        - Add Node to Cluster (namefromcluster)

- Apply OS configuration with Puppet

- Add SSH to Node

- Add JVM to Node

- Deploy last app version with Fabric

- Configure Apache with Fabric

- Configure elastic load balancer