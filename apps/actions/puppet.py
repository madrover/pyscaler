"""
**puppet.py** is a Fabric fabfile used to send puppet manifests to a remote host and execute them.
"""

from fabric.api import put, run, sudo

def deploy_puppetfile(puppetfile):
    put(puppetfile,"/tmp")
    sudo("puppet  apply "+ puppetfile)
    

