#-*- coding=utf-8 -*-
from django.conf.urls import patterns, include, url
from secondhand.BasicViews import *
from secondhand.UserViews import *
from secondhand.ProductViews import *
from secondhand.Test import *
from django.contrib import admin
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'se.views.home', name='home'),
    # url(r'^se/', include('se.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^admin/',include(admin.site.urls)),
)

urlpatterns += patterns('secondhand.ProductViews',
	(r'^$|^index/$', index),
	(r'^product/(\d+)/$', LoginRequired(ProductInfo)),
	(r'^product/add/$', LoginRequired(AddProduct)),
	(r'^search/$', Search),
)
urlpatterns += patterns('secondhand.UserView',
	(r'^login/$', Login),
	(r'^logout/$', LoginRequired(Logout)),
	(r'^editpro/$', LoginRequired(EditPro)),
	(r'^register/$', Register),
	(r'^profile/(\d+)/$', LoginRequired(ShowUser)),
)
urlpatterns += patterns('secondhand.Test',
		(r'^test/$', Test),
)
#urlpatterns += patterns('',
		#(r'^(?P<path>.*)$','django.views.static.serve',
		# {
		# 	'document_root':'/home/se/se/secondhand/templates'}
		#),
#)
