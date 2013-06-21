from fabric.api import run,cd,sudo,put

def initialsetup():
    sudo("mkdir -p /tools/scripts")
    put('/opt/django/pyscaler/scripts/*',"/tools/scripts",use_sudo=True,mode=0777)
    
        
    