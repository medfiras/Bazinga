from django.conf import settings
from django.conf.urls import patterns, include, url


from django.contrib import admin

# from profile.forms import SignupFormExtra
from django.contrib.auth.decorators import login_required

from bazinga.views import *
from projects.views import *

# from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from userena import views as userena_views
from userena import settings as userena_settings
from accounts.forms import *
# import autocomplete_light.shortcuts as al


# al.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

# al.registry.autocomplete_model_base = User
# al.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bazinga.views.home', name='home'),
    # url(r'^bazinga/', include('bazinga.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view() , name='home'),
    # url(r'^projects/', Project().List_all_project , name='List_all_project'),
    url(r'^projects/', Project().get_repo_info , name='get_repo_info'),
    url(r'^details/', Project().get_repo_details, name='get_repo_details'),

    url(r'^accounts/', include('userena.urls')),
    # url(r'^messages/', include('userena.contrib.umessages.urls')),
    url(r'^messages/', include('django_messages.urls')),
    # url(r'^events/', include('event_rsvp.urls')),
    url(r'^todolist/', include('todolist.urls')),
    

    # url(r'^(?P<username>[\.\w]+)/edit/$',userena_views.profile_edit, {'template_name': 'userena/profile_form.html'},name='userena_profile_edit'),
    url(r'^(?P<username>[\@\.\w-]+)/password/$', userena_views.password_change, {'template_name': 'userena/profile_form.html'}, name="userena_password_change"),
    url(r'^(?P<username>[\@\.\w-]+)/email/$', userena_views.email_change, {'template_name': 'userena/profile_form.html'}, name='userena_email_change'),
    url(r'^(?P<username>[\.\w-]+)/edit/$','userena.views.profile_edit',{'edit_profile_form': CustomEditProfileForm,'template_name': 'userena/profile_form.html'},name='userena_profile_edit'),

    url(r'^todo/', todolist, name='todo'),
    url(r'^addtodo/$', addTodo, name='addtodo'),
    url(r'^todofinish/(?P<id>\d+)/$', todofinish, name='finish'),
    url(r'^todobackout/(?P<id>\d+)/$', todoback,  name='backout'),
    url(r'^updatetodo/(?P<id>\d+)/$', updatetodo, name='update'),
    url(r'^tododelete/(?P<id>\d+)/$', tododelete, name='delete'),

    # url(r'^autocomplete/', include('autocomplete_light.urls')),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
else:
    print "no server is configured to serve media files. Do it now."