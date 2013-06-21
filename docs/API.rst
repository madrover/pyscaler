API
=======

PyScaler uses its own API to trigger any action or request any information.  

PyScaler API is REST based, with clear urls and with all the parameters in the url itself.

The API answers are alway in JSON format dues its easy readability. All API
requests are use the GET http verb to improve its readability as well.

What most of the API calls do is trigger a Celery task as the requested action
is executed asynchronously. Because of that the typical API have got two parts:

- First call is the action request:
  
  ::
    
    http://pyscaler:8000/actions/ec2node/remove/cluster/ec2/node/ec201/
  
  It will return the Celery task id:

  :: 
   
    {"taskid": "20d0d58e-0fa2-4a47-929f-d8ea88d18dd8"}

- Second call is the request output:
  
  ::
    
    http://jmxscaler:8000/actions/ec2node/output/20d0d58e-0fa2-4a47-929f-d8ea88d18dd8/
  
  If the Celery task has not finished it will answer something like  the following:

  :: 
   
    {"state": "PENDING", "result": null, "taskid": "20d0d58e-0fa2-4a47-929f-d8ea88d18dd8"}
 
  Once the Celery task is finished it will return the Celery task output.

  ::
   
    {"state": "SUCCESS", "result": "Node ec201 from cluster ec2 deleted.",
    "taskid": "20d0d58e-0fa2-4a47-929f-d8ea88d18dd8"}

The typical interaction that PyScaler web fronted do is first request an action via a 
jquery url call, then use jquery to call many times the output url until its state
has changed and then show its output on the web page.