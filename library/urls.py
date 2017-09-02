from django.conf.urls import url, include
from django.contrib import admin
from issueServer.views import checkOutView, checkInView
from readwrite.views import readWriteView, userLoginView, userLogoutView, homeView
admin.site.site_header = "NITC CENTRAL LIBRARY ADMINISTRATION"
admin.site.index_title = "NITC CENTRAL LIBRARY ADMINISTRATION"
admin.site.site_title = "NITC CENTRAL LIBRARY ADMINISTRATION"
urlpatterns = [
	url(r'^$', homeView, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^CHECKOUT/(?P<device_id>[A-Za-z0-9]+)/$', checkOutView),
    url(r'^CHECKIN/(?P<device_id>[A-Za-z0-9]+)/$', checkInView),
    url(r'^readwrite/$', readWriteView, name='readwrite'),
    url(r'^login/$', userLoginView, name='login'),
    url(r'^logout/$', userLogoutView, name='logout')
]
