from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render 

 
@login_required
def administration(request):
    '''
    This view integrates the native django admin pages into PyScaler's user interface.
    '''
    #return redirect('/admin/')
    return render(request, 'administration.html')
