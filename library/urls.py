from django.conf.urls import url, include
from django.contrib import admin
from issueServer.views import checkOutView, checkInView
from readwrite.views import readwrite_view, user_login, user_logout, home
admin.site.site_header = "NITC CENTRAL LIBRARY ADMINISTRATION"
admin.site.index_title = "NITC CENTRAL LIBRARY ADMINISTRATION"
admin.site.site_title = "NITC CENTRAL LIBRARY ADMINISTRATION"
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^CHECKOUT/(?P<device_id>[A-Za-z0-9]+)/$', checkOutView),
    url(r'^CHECKIN/(?P<device_id>[A-Za-z0-9]+)/$', checkInView),
    url(r'^readwrite/$', readwrite_view, name='readwrite'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^$', home, name='home')
]
