High Availability
==================

PyScaler can achieve high availability by:

- Deploy Django application in a secondary node
- Use a load balancer in front of the http port
- Configure Django to use MySql instead of SqLite
- Configure both Django nodes to use MySql
- MySql can be configured in `cluster <http://www.mysql.com/products/cluster/>`_, as well
- Enable RabbitMQ `clustering <http://www.rabbitmq.com/clustering.html>`_
- USe a single memcached instance for all django servers.
- Memcached can be `clustered <http://www.slideshare.net/gear6memcached/implementing-high-availability-services-for-memcached-1911077>`_, as well 
 
 