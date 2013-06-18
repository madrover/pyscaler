Installation steps
====================================

The following steps describe  the installation of PyScaler on a Centos 6 box.

- Install EPEL repository

  ::
    
    rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

- Install required packages

  ::

    yum install httpd mod_wsgi tomcat6-webapps tomcat6 python-pip librabbitmq \ 
    rabbitmq-server.noarch make gcc gcc-c++ java-1.6.0-openjdk-devel \ 
    java-1.6.0-openjdk git sqlite memcached nginx

- Enable and start services
	
  ::

    chkconfig memcached on
    /etc/init.d/memcached start
    chkconfig rabbitmq-server on
    /etc/init.d/rabbitmq-server

- Install the virtualenv packages to ease the python libraries management

  ::

    pip-python install virtualenv
    pip-python install virtualenvwrapper
	
- Create a new virtualenv

  ::

    mkvirtualenv pyscaler
	
- Create the pyscaler folder

  ::

    mkdir -p /opt/django/pyscaler
	
- Create the celery logs folder

  ::	

    mkdir /var/log/celery
    chown pyscaler:pyscaler  /var/log/celery
    mkdir /var/run/celery
    chown pyscaler:pyscaler  /var/run/celery

- Grab the latest PyScaler version from github

 ::

   cd /opt/django/pyscaler
   git clone https://www.github.com/madrover/pyscaler.git

- Jpype python lib needs Java JDK to be installed and have JAVA_HOME 
  defined to build correctly. More details `here <http://thomas-cokelaer.info/blog/2012/10/installing-jpype-to-use-java-from-python/>`_.

  export JAVA_HOME=/usr/lib/jvm/java-1.6.0-openjdk.x86_64/

- Install pyscaler python lib requirements

 ::
   
   pip install -r requirements.txt

- Configure Nginx to forward requests to Django / Gunicorn. There is a good guide `here. <http://honza.ca/2011/05/deploying-django-with-nginx-and-gunicorn>`_


This is an example nginx configuration

 :: 

  upstream app_server_djangoapp {
      server localhost:8000 fail_timeout=0;
  }
  
  server {
      listen 80;
      server_name pyscaler;
  
      access_log  /var/log/nginx/guni-access.log;
      error_log  /var/log/nginx/guni-error.log info;
  
      keepalive_timeout 5;
  
      root /opt/django/pyscaler/pyscaler;
  
      location /static {    
          autoindex on;    
          alias/opt/django/pyscaler/pyscaler/site_media/static;    
      }
  
      location /media {
         autoindex on;
         alias /opt/django/pyscaler/pyscaler/site_media/media;
      }
  
      location / {
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header Host $http_host;
          proxy_redirect off;
  
          if (!-f $request_filename) {
              proxy_pass http://app_server_djangoapp;
              break;
          }
      }
  }