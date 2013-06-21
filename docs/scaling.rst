Scaling
========

PyScaler provides the infrastructure needed to automate the deployment of new
nodes in an cloud based cluster.

The deployment of a new node can be triggered manually or automatically due 
a monitoring trigger.

The creation a of a new node into a cluster uses the following components:

- IaaS provider API to automate the execution of a new virtual machine.
- Puppet to provision the new virtual machine with a specific operating system configuration.
- Fabric to automate the deployment of new applications an other automatisms

Deployment steps
-----------------------------------
This sections describes the steps needed to deploy a new node

+--------------------------------------------------+--------------------------------------------+
| STEP                                             |                                            |
+==================================================+============================================+
| Deploy a new VM on EC2 (clustername,user, )      | DeployEC2Node action                       |
+--------------------------------------------------+--------------------------------------------+
| Add the node to the Elastic Load Balancer        | DeployEC2Node action                       |
+--------------------------------------------------+--------------------------------------------+
| Operating system configuration and provisioning  | OSConfiguration action                     |
+--------------------------------------------------+--------------------------------------------+
| Tomcat configuration                             | LocalScript or DistributeScript actions    |
+--------------------------------------------------+--------------------------------------------+
| Application deployment                           | LocalScript or DistributeScript actions    |                   
+--------------------------------------------------+--------------------------------------------+
| Cluster update                                   | LocalScript or DistributeScript actions    |
+--------------------------------------------------+--------------------------------------------+
| Notification                                     | Email action                               |
+--------------------------------------------------+--------------------------------------------+

The PyScaler distribution contains some Puppet and Fabric scripts that can be
used to automate a Tomcat deployment.