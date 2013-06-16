Features
===============

- **Monitoring** 
   PyScaler is able to monitor remote hosts and store the performance 
   data for further analysis and business logic. 

 - **SSH monitoring**

   PyScaler can connect to remote hosts via SSH, execute scripts to gather 
   performance data and index its output.

 - **JMX monitoring**

   PyScaler can connect to remote JVMs via JMX and gather performance data
   via the exposed mbeans.  

 - **Counter graphs**
   
   The performance data can be easily visualized using available graphs. 
   There are different graphs per monitored target and counters.

- **Control**
   PySCaler can be execute actions against its managed nodes. These action
   can be execute manually or triggered automatically when defined 
   performance thresholds are hit.

 - **Remote command execution**
   
   It can execute command locally on specific nodes or on all the nodes 
   from a cluster.

 - **Fabric scripts execution**
   
   It can execute Fabric scripts that can be used to execute local or 
   remote shell commands (normally or via sudo) and uploading/downloading
   files, as well as auxiliary functionality such as prompting the 
   running user for input, or aborting execution. 
   
 - **Triggers**
   
   PyScaler can analyze available performance data and automatically trigger
   defined actions when a performance threshold is reached during a certain
   amount of time.

- **Provisioning**
   PyScaler can be used to provision new servers.

 - **EC2 node deployment**
   
   PyScaler can launch new Amazon EC2 instances with defined parameters.

 - **Operating system configuration**
   
   PyScaler can provision nodes using Puppet.

- **Deployment scaling**
  
  The previously explained features (monitoring, control and provisioning) 
  can be used together to automatically scale a cloud based cluster.
  PyScaler will monitor the cluster and when a defined performance threshold 
  is reached then the necessary actions to deploy a new cluster node will  
  be executed, thus scaling it.

- **High availability**

  Each component of PyScaler is designed to be highly available.