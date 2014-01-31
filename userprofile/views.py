from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def user_profile(request, user_name):
    context = {}
    context.update(csrf(request))
    form = UserProfileForm()
    context['form'] = form
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/%s' % request.user.username)
        else:
            form = UserProfileForm(instance=request.user.profile)
            context['form'] = form
    context['login_mode'] = True
    context['user'] = request.user
    if request.user.is_superuser:
            context['user_admin'] = True

    return render_to_response('user/edit-profile.html', context)

# Create your views here.
