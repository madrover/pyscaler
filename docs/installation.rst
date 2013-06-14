Installation steps
====================================

The following steps describe  the installation of PyScaler on a Centos 6 box.

- Install EPEL repository

	rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

- Install required packages

	yum install httpd mod_wsgi tomcat6-webapps tomcat6 python-pip librabbitmq rabbitmq-server.noarch make gcc gcc-c++ java-1.6.0-openjdk-devel java-1.6.0-openjdk git sqlite

- Install the virtualenv packages to ease the python libraries management

	pip-python install virtualenv
	pip-python install virtualenvwrapper
	
- Create a new virtualenv

	mkvirtualenv pyscaler
	
- Create the pyscaler folder

	mkdir -p /opt/django/pyscaler
	
- Grab the latest PyScaler version from github

	cd /opt/django/pyscaler
	git clone https://www.github.com/madrover/pyscaler.git
	
