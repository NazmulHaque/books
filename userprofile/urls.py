from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^edit-profile/$', 'userprofile.views.user_profile'),
    url(r'^(?P<user_name>\w+)/$', 'books.views.index'),
    url(r'^update-basic-info/$', 'userprofile.views.update_basic_info'),
    url(r'^update-profile-photo/$', 'userprofile.views.update_profile_photo'),
    url(r'^change-password/$', 'userprofile.views.change_password'),
)