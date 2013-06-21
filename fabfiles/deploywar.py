from fabric.api import run,cd,sudo,settings

def deploywar():
    with cd("/tmp"):
        run("wget http://tomcat.apache.org/tomcat-6.0-doc/appdev/sample/sample.war")
        sudo("chown tomcat:tomcat sample.war")
        sudo("mv sample.war /usr/share/tomcat6/webapps/test.war")
        with settings(warn_only=True):
            sudo("ps -ef | grep java | awk '{print $2}' | xargs kill -9")
        sudo("/etc/init.d/tomcat6 start")
    