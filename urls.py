from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to, direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from track import views
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    (r'^%s$' % settings.SITE_CODE, direct_to_template, {'template':'error.html', 'extra_context': {'site_code': settings.SITE_CODE}}),
    (r'^error_test$', direct_to_template, {'template':'error_test.html'}),
    url(r'^%s/t/error$' % settings.SITE_CODE, views.error, name='api_error'),
    url(r'^t/error_track$', views.error_track, name='api_error_track'),
    url(r'^js/error_track.js$', views.error_js, name='error_js'),

    (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
