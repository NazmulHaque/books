from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^add/$', 'products.views.add'),
    url(r'^(?P<product_id>\d+)/$', 'products.views.product_view'),
    url(r'^(?P<product_id>\d+)/edit/$', 'products.views.info_edit'),

)