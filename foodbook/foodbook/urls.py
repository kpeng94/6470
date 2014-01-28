from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import search_global, save_settings, register_view, display_other_profile, display_user_settings, display_normal_recipe, display_user_profile, home, login_user, register, default_page, logout_user, show_ingredient, search_ingredients, add_recipe, list_my_recipes
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
    url(r'^recipe/([0-9]+)$', display_normal_recipe),
    url(r'^recipe/add[/]?$', add_recipe),
    url(r'^recipe/edit$', add_recipe),
    url(r'^recipe', list_my_recipes),
    #url(r'^ingredients[/]?$', search_ingredients),
    #url(r'^ingredients/([a-zA-Z]+)$', show_ingredient),
    url(r'^home$', home),
    url(r'^search$', search_global),
    url(r'^register/try$', register),
    url(r'^register$', register_view),
    url(r'^login$', login_user),
    url(r'^logout$', logout_user),
    url(r'^user[/]?$', display_user_profile),
    url(r'^user/([a-zA-Z0-9]+)$', display_other_profile),
    url(r'^settings/save$', save_settings),
    url(r'^settings$', display_user_settings),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'', default_page),
)