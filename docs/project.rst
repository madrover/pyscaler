PyScaler Project
=======

Introduction
------------------

In the last few years we have seen a new computing area that is becoming
increasingly relevant in today’s IT ecosystem. This area is called the
Cloud.

Cloud technologies are a new paradigm of computing that totally changes
the way we have been thinking about computers. `John
Gage <http://en.wikipedia.org/wiki/John_Gage>`_\ ’s 1984 prophetic
phrase “The network is the computer“ is now becoming more real than
ever. In fact, we can hack it an actualize it to a more contemporary
version. Now, the cloud is the computer. And with such a gigantic step
on how we deal with computers it is inevitable to be interested in.

Cloud technologies can come in many forms. However we can classify the
main types of cloud services as:

#. **Infrastructure as a service (IaaS)** Where the provider offers dynamic
   access to computers, typically virtual machines, and other related
   resources such as storage, messaging, etc... This is the lower level
   form of cloud services. An example of IaaS is `Amazon
   EC2 <http://aws.amazon.com/ec2/>`_.
#. **Platform as a service (PaaS)** Where the provider offers a higher level
   platform typically including an operating system, a programming
   language execution environment, a database, and a web server. An
   example of PaaS is `Google App
   Engine. <https://developers.google.com/appengine/>`_
#. **Software as a service (SaaS)** Where the provider offers application
   level software. Whereas IaaS and PaaS services are low level services
   addressed to be building block to construct other services, SaaS
   services are usually addressed to be used directly by final users. An
   example of SaaS is `Salesforce <http://www.salesforce.com>`_.

This service classification is done from lower to higher level. In fact,
higher level services are often built using lower level services.
However, all these implementations share a common set of technologies
and procedures.

Cloud technologies are heavily based on virtualization and `autonomic
computing <http://en.wikipedia.org/wiki/Autonomic_computing>`_. With the
help of them the cloud infrastructures can leverage existing commodity
hardware, lower costs and ease its usage. This way, the entrance
barriers to create new projects are lower than ever.

In this project we will focus both in virtualization and autonomic
computing as we want to use the IaaS services capabilities to automate
the behavior of an IT deployment. We want to create a system that is
able to enlarge or reduce a cluster based on certain performance events.

Motivation
------------------

During my latest career years I have been involved in many projects
related to J2EE and web technologies. I have been specializing in
systems administration with a special love for high availability and
performance matters. With the raise of the cloud technologies I have
been interested in how joining the J2EE and cloud stacks can provide
flexible, performant and reliable environments.

Until now when you had to provision an environment you had to keep in
mind the maximum number of concurrent users and then do an appropriate
hardware sizing that is able to handle the load. Besides that, there
were other concerns as the high availability matters.

Finally, what usually happens is that you end up with some very big
computers that have costed a lot of money and are often underused. This
approach is inflexible and expensive.

It can happen that your application has got utilization peaks that
happen a few times a week but you don’t know when. In pre cloud
deployments you would be tied to have servers big enough to handle the
utilization peaks but that would be mostly underused.

One of the big points of the cloud service providers is the pay as you
go schema. This feature together with the ability to start and stop
servers on demand can help you reduce the deployment costs thus enabling
the environment to automatically respond to the user load behavior.

Project description
-----------------------

This project aims to create a system that is able to horizontally scale
a J2EE based environment when certain OS or JVM thresholds are reached.

To achieve this goal we will build a service that is able to gather
performance statistics of a number of machines and execute actions when
certain events are reached. The events are can be performance thresholds
or system events. The actions are the steps needed to provision a new
cluster node and integrate it into the cluster.

There are different components that must be created:

- A remote performance monitor
- A performance counters analyzer that is able to apply some business logic
- A module to automate the deployment of a new virtual machines
- A module that is able to provision the virtual machine
- A module that is able to integrate the virtual machine in an existing cluster

Objectives
------------------

The objectives that we are trying to achieve with this project are:

- Create a tool that is able to enhance scalability capabilities of a cloud
  based J2EE environment.
- The tool itself must be deployable on a cloud environment and have high
  availability and scalability features.
- Gain knowledge on cloud architectures
- Learn how to use an IaaS provider and its API
- Use provisioning tools to automate the  deployment of a cluster
- Understand the performance metrics of a J2EE server
- Be able to create a business logic that is able to analyze events over time
- Although the tool is aimed to analyze J2EE performance metric and make use 
  of one specific IaaS provider it should be designed to easily deploy
  new performance counter sources and IaaS providers


Risk analysis
------------------

The main risks associated with the project are the following. We
provide, as well, an associated action designed to avoid them or, if
they do not achieve it, alleviate it.

+--------------------------------------+-------------+--------+-----------------------------------------------------------+
| RISK                                 | PROBABILITY | IMPACT | ACTION                                                    |
+======================================+=============+========+===========================================================+
| Too many technologies and components | High        | High   | - Design the environment as simple as possible.           |
| to manage and integrate.             |             |        | - Focus on a single IaaS environment.                     |
|                                      |             |        | - Focus on a simple J2EE server and application to deploy |
+--------------------------------------+-------------+--------+-----------------------------------------------------------+
| As the application will be used in a | High        | Medium | Develop when possible with local servers and the use paid |
| public cloud provider with costs     |             |        | services only to test when needed                         |
| associated to the server time usage  |             |        |                                                           |
+--------------------------------------+-------------+--------+-----------------------------------------------------------+
|The complexity of the project and the | High        | High   | Define a realist project schedule and try to follow it as |
|tight schedule                        |             |        | strictly as possible                                      |
+--------------------------------------+-------------+--------+-----------------------------------------------------------+

Scope
------------------

Although the service is aimed to be open, modular and expandable due to
time constraint we need to focus on certain premises.

- Integration with only one IaaS service
- Scale one J2EE container
- Scale one J2EE application 
- Scale one web server frontend

Planning
------------------

The project has got the following organization.

Activities
~~~~~~~~~~~~~

The project is divided in the following activities:

- **Analysis**

 - **Design** Design the solution
 - **Proof Of Concept** Create an initial POC to ensure the proposed solution is valid

- **Development**

 - **Monitoring module** Create the module that monitors the environment to be scaled
 - **Control module** Create the module that handles the application business logic
 - **Action module** Create the module that triggers the scalation

- **Deployment**

 - **Virtual machine deployment** Automate the deployment of new computers
 - **J2EE Application provisioning** Automate the J2EE application cluster deployment
 - **Web server integration** Automate the clustered web server configuration

- **Testing** Quality assurance
- **Documentation** Document the project

Human resources
~~~~~~~~~~~~~~~~~~~~~~~~~~

The following profiles are needed to achieve this project

#. Analyst. Defining and documenting the project
#. Developer. Develop the server
#. Systems Administrator. Integrate the server with the existing IaaS
   provider and provision the application to be scaled
#. Test Engineer Perform the quality assurance and testing processes to
   ensure the correct behavior of the service

IT Resources
~~~~~~~~~~~~~~~~~~~~~~~~~~

The project will be mostly developed on local development computer.
However, to truly test the service we will use an online IaaS provider
(Amazon AWS).

Effort estimation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project timings are tied to the UOC semester timings and
constraints. Because of that, we try to align the beginning and end to
the academic course. We assume working from Monday to Friday and
skipping the public holidays.

The following table contains the project calendar and assigned resource
per activity.

+-------------------------------+-------------+---------------+------+--------------------------+
| TASKS                         | INIT DATE   | END DATE      | DAYS | RESOURCE                 |
+===============================+=============+===============+======+==========================+
| **Analysis**                  |             |               |      |                          |
+-------------------------------+-------------+---------------+------+--------------------------+
| Design                        | 14/03/2013  | 27/03/2013    | 10   | Analyst                  |
+-------------------------------+-------------+---------------+------+--------------------------+
| Proof of concept              | 2/04/2013   | 15/04/2013    | 10   | Developer                |
+-------------------------------+-------------+---------------+------+--------------------------+
| **Development**               |             |               |      |                          |
+-------------------------------+-------------+---------------+------+--------------------------+
| Monitoring module             | 16/04/2013  | 29/05/2013    | 10   | Developer                |
+-------------------------------+-------------+---------------+------+--------------------------+
| Control module                | 30/04/2013  | 14/05/2013    | 10   | Developer                |
+-------------------------------+-------------+---------------+------+--------------------------+
| Actions module                | 15/05/2013  | 21/05/2013    | 5    | Developer                |
+-------------------------------+-------------+---------------+------+--------------------------+
| **Integration**               |             |               |      |                          |
+-------------------------------+-------------+---------------+------+--------------------------+
| Virtual machine deployment    | 22/05/2013  | 27/05/2013    | 3    | Systems Administrator    |
+-------------------------------+-------------+---------------+------+--------------------------+
| J2EE application deployment   | 28/05/2013  | 30/05/2013    | 3    | Systems Administrator    |
+-------------------------------+-------------+---------------+------+--------------------------+
| Web server Integration        | 31/05/2013  | 31/05/2013    | 2    | Systems Administrator    |
+-------------------------------+-------------+---------------+------+--------------------------+
| **Testing**                   | 3/06/2013   | 14/06/2013    | 10   | Test Engineer            |
+-------------------------------+-------------+---------------+------+--------------------------+
| **Documentation**             | 17/06/2013  | 21/06/2013    | 5    | Analyst                  |
+-------------------------------+-------------+---------------+------+--------------------------+

The TFC subject has got 7,5 credits and each credit should have around
25 hours of dedication (25x7,5 = 187,5). Based in that calculation we
have defined the following daily effort.

+------------+-----+
| TOTAL TIME |     | 
+============+=====+
| Days       | 68  |
+------------+-----+
| Hours/day  | 3   |
+------------+-----+
| Hours      | 204 |
+------------+-----+

The following image is the project’s Gannt diagram.


.. figure:: images/gantt.png
   :align: center
   :alt: 
   :scale: 75 %

Economic evaluation
------------------------ 

There are two type of costs associated with the the project, human and
computing resources.

The human resources costs are based detailed in the following table:

+-----------------------+---------+-----------+-------+
| COSTS                 | HOURS   | RATE/HOUR | COST  |
+=======================+=========+===========+=======+
| Analyst               | 45      | 50€       | 2250€ |
+-----------------------+---------+-----------+-------+
| Developer             | 105     | 30€       | 3150€ |
+-----------------------+---------+-----------+-------+
| Systems Administrator | 24      | 35€       | 840€  |
+-----------------------+---------+-----------+-------+
| Test Engineer         | 30      | 30€       | 900€  |
+-----------------------+---------+-----------+-------+
|                       |         | **TOTAL** | 7140€ |
+-----------------------+---------+-----------+-------+

The initial computing resources are already in place as we own the
development computer.

To test the service on a cloud environment we need to contract the
services of an IaaS provider. However, we will use the Amazon AWS Free
Usage Tier so it should be free while developing the project.