import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import *
#from django.template import RequestContext

from django.contrib.auth.forms import AuthenticationForm
from forms import RegistrationForm, LoginForm
from utils import JSONEncoder

def home(request):
    #import pdb;pdb.set_trace()
    if request.user.is_authenticated():
        return redirect('/user/%s' % request.user.username)

    context = {}
    context.update(csrf(request))
    signup_form = RegistrationForm()
    context['signup_form'] = signup_form

    return render_to_response('home.html', context)


def signup(request):
    if request.user.is_authenticated():
        return redirect('/user/%s' % request.user.username)
    else:
        if request.method == 'POST':
            form = RegistrationForm(data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('true')
            else:
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)
                data = json.dumps(errors_dict, cls=JSONEncoder)
                return HttpResponse(data, content_type="application/json")


def signup_success(request):
    if request.user.is_authenticated():
        return redirect('/user/%s' % request.user.username)
    else:
        return render_to_response('user/thanks.html')


def login(request):
    """
    Displays the login form and handles the login action.
    """
    if request.user.is_authenticated():
        return redirect('/user/%s' % request.user.username)

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth.login(request, user)
                dict = {'login': True, 'username': user.username}

                data = json.dumps(dict, cls=JSONEncoder)
                return HttpResponse(data, content_type="application/json")

            else:
                dict = {'login': False, 'errors': "Please enter a correct email and password."}
                data = json.dumps(dict, cls=JSONEncoder)
                return HttpResponse(data, content_type="application/json")
        else:
            dict = {'login': False, 'errors': form.errors}

            data = json.dumps(dict, cls=JSONEncoder)
            return HttpResponse(data, content_type="application/json")


@login_required(login_url='/')
def index(request, user_name):
    if user_name == request.user.username:
        context = {
            'user': request.user,
            'login_mode': True
        }
        if request.user.is_superuser:
            context['user_admin'] = True

        return render_to_response('user/index.html', context)
    else:
        return redirect('/user/%s' % request.user.username)


@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return redirect('/')