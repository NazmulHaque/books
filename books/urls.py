from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^user/', include('userprofile.urls')),
    url(r'^product/', include('products.urls')),
    url(r'^$', 'books.views.home'),
    url(r'^login-view/$', 'books.views.login_view'),
    url(r'^login/$', 'books.views.login'),
    url(r'^logout/$', 'books.views.logout'),
    url(r'^signup/$', 'books.views.signup'),
    url(r'^search/all$', 'products.views.search'),
    url(r'^search-result/$', 'products.views.search_result'),
    url(r'^recent-search/$', 'products.views.recent_search'),

    # url(r'^books/', include('books.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
