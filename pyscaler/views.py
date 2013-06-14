from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render 

 
@login_required
def administration(request):
    #return redirect('/admin/')
    return render(request, 'administration.html')
