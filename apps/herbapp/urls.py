from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tastypie.api import Api
from herbapp.api.resources import *
from herbapp.views import *

# RESTful API
v1_api = Api(api_name='v1')
v1_api.register(PurchaseResource())
v1_api.register(AuthorResource())
v1_api.register(DiseaseResource())
v1_api.register(HerbResource())
v1_api.register(HerbPictureResource())
v1_api.register(HerbUsageResource())
v1_api.register(HerbPickResource())


# URLconf
urlpatterns = patterns('',

    (r'^api/', include(v1_api.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', 'herbapp.views.index'),

) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + staticfiles_urlpatterns()


