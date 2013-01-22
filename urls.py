from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()

urlpatterns = patterns('',

    # administration
    (r'^admin/', include(admin.site.urls)),

    # allow robots
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /api\n", mimetype="text/plain")),

    # herbalist app
    (r'^', include('herbapp.urls')),
)


