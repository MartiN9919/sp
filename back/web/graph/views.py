from django.shortcuts import render  # redirect
from django.contrib.auth.decorators import login_required
from django.contrib   import auth
from django.conf      import settings


@login_required(login_url='/auth/login/')
def main(request):
    usr = auth.get_user(request)
    if usr.is_authenticated: sInfo = usr.first_name+' '+usr.last_name
    else: sInfo = ''
    return render(request, 'graph.html', {'pag_title': settings.PROJECT_TITLE_NAME, 'username': sInfo} )
