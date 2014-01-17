from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import showHome, test_login, register, default_page, logout_user
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'foodbook.views.home', name='home'),
    # url(r'^foodbook/', include('foodbook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home$', test_login),
    url(r'^register$', register),
    url(r'^logout$', logout_user),
    url(r'', default_page),
)
