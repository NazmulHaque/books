from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'books.views.home'),
    url(r'^user/(?P<user_name>\w+)/edit_profile/$', 'userprofile.views.user_profile'),
    url(r'^user/(?P<user_name>\w+)/$', 'books.views.index'),
    url(r'^login/$', 'books.views.login'),
    url(r'^logout/$', 'books.views.logout'),
    url(r'^signup/$', 'books.views.signup'),
    url(r'^thanks/$', 'books.views.signup_success'),

    # url(r'^books/', include('books.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)