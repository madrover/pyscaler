from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.control import tasks 

@login_required
def index(request):
    """
    Shows initial monitoring page
    """
    tasks.getTriggerCounters()
    
    return render(request, 'monitoring.html')