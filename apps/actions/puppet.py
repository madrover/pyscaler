"""
**puppet.py** is a Fabric fabfile used to send puppet manifests to a remote host and execute them.
"""

from fabric.api import put, run, sudo, env

env.warn_only = True

def deploy_puppetfile(puppetfile):
    
    out = sudo('which puppet')
    if out.find("no puppet in") != -1 :
        print "puppet not found, installing it"
        sudo("yum -y install puppet")
    put(puppetfile,"/tmp")
    puppetfile = puppetfile.split("/")[-1]
    sudo("puppet  apply  /tmp/"+ puppetfile)
    sudo("rm /tmp/" + puppetfile)
    

