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
from userprofile.models import UserProfile


def home(request):
    #import pdb;pdb.set_trace()
    if request.user.is_authenticated():
        return redirect('/user/%s' % request.user.username)

    context = {}
    context.update(csrf(request))
    signup_form = RegistrationForm()
    context['signup_form'] = signup_form

    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = RegistrationForm(request.POST)
            context['signup_form'] = signup_form
            if signup_form.is_valid():
                signup_form.save()
                return redirect('/thanks')
        elif 'login' in request.POST:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/user/%s' % request.user.username)
    return render_to_response('home.html', context)


def signup(request):
    if request.user.is_authenticated():
        return redirect('/user/%s' % request.user.username)
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/thanks')
        else:
            return redirect('/')


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
        return  HttpResponse('true');

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            return HttpResponse(('true'), request.session, user)
        else:
            template = "user/login-form.html"
    else:
        form = LoginForm()
        template = "users/login.html"
    return TemplateResponse(request, template, {'form': form})


@login_required(login_url='/')
def index(request, user_name):
    if user_name == request.user.username:
        context = {
            'user': request.user,
            'login_mode': True
        }
        if UserProfile.objects.filter(user=request.user).count():
            userprofile = UserProfile.objects.get(user=request.user)
            context['userprofile'] = userprofile

        return render_to_response('user/index.html', context)
    else:
        return redirect('/user/%s' % request.user.username)


@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return redirect('/')