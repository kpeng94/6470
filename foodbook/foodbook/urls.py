from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import home, login_user, register, default_page, logout_user, show_ingredient, search_ingredients, add_recipe, list_my_recipes
admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'foodbook.views.home', name='home'),
    # url(r'^foodbook/', include('foodbook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin', include(admin.site.urls)),
    url(r'^recipe/add[/]?$', add_recipe),
    url(r'^recipe/edit$', add_recipe),
    url(r'^recipe', list_my_recipes),
    url(r'^ingredients[/]?$', search_ingredients),
    url(r'^ingredients/([a-zA-Z]+)$', show_ingredient),
    url(r'^home$', home),
    url(r'^register$', register),
    url(r'^login$', login_user),
    url(r'^logout$', logout_user),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'', default_page),
)