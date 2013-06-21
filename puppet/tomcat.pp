  Package { # defaults
    ensure => installed,
  }
   $packages = [ "tomcat6", "httpd","tomcat6-webapps","tomcat6-admin-webapps"]
    package { $packages: }
 
  file { "/etc/tomcat6/tomcat-users.xml":
    owner => 'root',
    require => Package['tomcat6'],
    notify => Service['tomcat6'],
  }
 
  file { '/etc/tomcat6/server.xml':
     owner => 'root',
     require => Package['tomcat6'],
     notify => Service['tomcat6'],
  }
  
  service { 'tomcat6':
    ensure => running,
    require => Package['tomcat6'],
  }
  
  service { 'httpd':
    ensure => running,
    require => Package['httpd'],
  }
  
  file { "/var/www/html/index.html":
    replace => "no", 
    ensure  => "present",
    content => "Index\n",
}

exec { "add_jmx_configuration":
	require => Package['tomcat6'],
    command => '/bin/echo "JAVA_OPTS=\"-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=18000 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl.need.client.auth=false -Djava.rmi.server.hostname=`curl http://169.254.169.254/latest/meta-data/public-hostname`\"" >> /etc/sysconfig/tomcat6',
    onlyif => [ 
                "/bin/grep -c com.sun.management.jmxremote  /etc/sysconfig/tomcat6 | /bin/grep 0"
              ]
}

  file { '/etc/sysconfig/tomcat6':
     owner => 'root',
     require => Package['tomcat6'],
     notify => Service['tomcat6'],
  }