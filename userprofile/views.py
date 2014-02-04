import json
import os

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist

from forms import UploadProfilePhoto, UserBasicInfoForm
from books.utils import JSONEncoder
from userprofile.models import UserProfile


@login_required(login_url='/')
def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect('/user/update-profile-first-time')
    else:
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
    form = UploadProfilePhoto()
    context['form'] = form

    if request.method == 'POST':
        form = UploadProfilePhoto(data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid():
            old_photo = UserProfile.objects.get(user=request.user).profile_photo
            if old_photo:
                os.remove(old_photo.file.name)
            form.save()
            return redirect('/user/edit-profile')
        else:
            return redirect('/user/edit-profile')
    if UserProfile.objects.filter(user=request.user).count():
        context['user_profile'] = UserProfile.objects.get(user=request.user)
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
    context = {}
    context.update(csrf(request))
    form = PasswordChangeForm(request.user)
    context['form'] = form

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
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
    return render_to_response('user-profile/change-password-form.html', context)


@login_required(login_url='/')
def update_basic_info_first_time(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        context = {}
        context.update(csrf(request))
        form = UserBasicInfoForm()
        context['form'] = form

        if request.user.is_authenticated():
            context['login_mode'] = True
        if request.method == 'POST':
            form = UserBasicInfoForm(data=request.POST, instance=request.user.profile)
            if form.is_valid():
                form.save()
                dict = {'submit': True, 'username': request.user.username}

                data = json.dumps(dict, cls=JSONEncoder)
                return HttpResponse(data, content_type="application/json")
            else:
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)
                data = json.dumps(errors_dict, cls=JSONEncoder)
                return HttpResponse(data, content_type="application/json")
        return render_to_response('user-profile/basic-info-first-time-form.html', context)
    else:
        return redirect('/user/' + request.user.username)

