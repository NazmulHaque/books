import json
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

from forms import UserProfileForm, UserBasicInfoForm
from books.utils import JSONEncoder
from userprofile.models import UserProfile


@login_required(login_url='/')
def user_profile(request):
    context = {}
    context['login_mode'] = True
    context['user'] = request.user
    if request.user.is_superuser:
        context['user_admin'] = True

    return render_to_response('user/edit-profile.html', context)



@login_required(login_url='/')
def update_profile_photo(request):
    context = {}
    context.update(csrf(request))
    form = UserProfileForm()
    context['form'] = form
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponse('true')
    return render_to_response('user-profile/profile-photo-form.html', context)


@login_required(login_url='/')
def update_basic_info(request):
    context = {}
    context.update(csrf(request))
    form = UserBasicInfoForm()
    context['form'] = form
    if request.method == 'POST':
        form = UserBasicInfoForm(data=request.POST, instance=request.user.profile)
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
    if UserProfile.objects.filter(user=request.user).count():
        context['user_profile'] = UserProfile.objects.get(user=request.user)
    return render_to_response('user-profile/basic-info-form.html', context)

@login_required(login_url='/')
def change_password(request):
    return render_to_response('user-profile/change-password-form.html')
# Create your views here.
