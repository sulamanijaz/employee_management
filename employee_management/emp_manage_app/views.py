from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.db.models import Q


def index_home(request):

    return render_to_response('employee/index.html', {
        'request': request,
    }, RequestContext(request, {}))


def login_user(request):
    if request.method == 'GET':
        return render_to_response('employee/login.html', {
            'request': request,
        }, RequestContext(request, {}))


# Create your views here.
