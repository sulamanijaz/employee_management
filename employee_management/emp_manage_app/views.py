from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.db.models import Q
from forms import userform
from django.contrib.auth.decorators import login_required


def index_home(request):

    return render_to_response('employee/index.html', {
        'request': request,
    }, RequestContext(request, {}))


def login_user(request):
    if request.method == 'POST':

        username = request.POST['email']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                variables = {
                    'form': userform
                }
                return render(request, 'employee/login.html', variables)
        else:
                # Bad login details were provided. So we can't log the user in.
                variables = {
                    'form': userform,
                    'message':"Email or password incorrect",
                    'email':username
                }
                return render(request, 'employee/login.html', variables)

                # The request is not a HTTP POST, so display the login form.
                # This scenario would most likely be a HTTP GET.
    else:
            # No context variables to pass to the template system, hence the
            # blank dictionary object...
            return render_to_response('employee/login.html', {
                'request': request, 'form': userform,
            }, RequestContext(request, {}))

@login_required
def user_home(request):
    return render_to_response('employee/home.html', {
        'request': request, 'form': userform,
    }, RequestContext(request, {}))


from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/home/')