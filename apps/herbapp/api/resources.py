import os
import random
import hashlib
import base64
import simplejson as json
from datetime import datetime
from functools import partial

from django.conf import settings
from django.http import HttpResponse
from django.contrib.sites.models import Site

from tastypie import fields
from tastypie.exceptions import NotFound
from tastypie.models import ApiKey
from tastypie.resources import Resource, ModelResource, ALL
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

from herbapp.models import Purchase, Author, Disease, Herb, HerbPicture, HerbUsage, HerbPick


# dehydrate helper for foreign key
def foreign_key_to_id(bundle, field_name):
    field = getattr(bundle.obj, field_name)
    field_id = getattr(field, '_id', None)
    return field_id


class TokenAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):

        try:
            token = request.GET.get('token')
            if token != "":
                purchase = Purchase.objects.get(token=token)
                return True
            return False
        except:
            return False


class PurchaseResource(ModelResource):
    """
    Purchase resource verifies customer purchase data. If the signature is OK,
    a new API key (token) is generated and sent to client in response.
    The token is necessary to access all other resources.

    """
    class Meta:
        queryset = Purchase.objects.all()
        fields = ['token','order']
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        resource_name = 'purchase'
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()

    def post_list(self, request=None, **kwargs):

        try:
            # parse JSON data from POST request
            data = json.loads(request.raw_post_data)
            purchase_data = data.get("inapp-purchase-data")
            data_signature = data.get("inapp-data-signature")

            # verify that signature is the result of signing the purchase data
            VERIFY_KEY = RSA.importKey(base64.decodestring(settings.PUBLIC_KEY))
            h = SHA.new(purchase_data)
            verifier = PKCS1_v1_5.new(VERIFY_KEY)
            signature = base64.decodestring(data_signature)
            verify_ok = verifier.verify(h, signature)
            
            if True: # TODO verify_ok

                # data / signature is correct
                ts = datetime.now()
                purchase_data_parsed = json.loads(purchase_data)
                order = purchase_data_parsed.get('orders')[0].get('orderId')
                token = hashlib.sha1(data_signature + str(random.random()) + ts.strftime("%Y%m%dT%H%M%S")).hexdigest()
                token_data = {"token" : token}

                # store or update token for related order ID
                purchase, created = Purchase.objects.get_or_create(order=order)
                purchase.order = order
                purchase.token = token
                purchase.app_platform = data.get('client-platform')
                purchase.app_version = data.get('client-version')
                purchase.app_language = data.get('client-language')
                purchase.screen_width = data.get('screen-width')
                purchase.last_sync_ts = ts
                purchase.counter = purchase.counter + 1
                purchase.save()
                
                status = 200
                if created:
                    status = 201
                
                # 200 OK / 201 Created (verification successful)
                response = HttpResponse(json.dumps(token_data) + "\n", mimetype="application/json", status=status)

            else:
            
                # 401 Unauthorized (verification failed)
                response = HttpResponse(status=401)

        except:

            # 400 Bad request (failed to parse the request)
            response = HttpResponse(status=400)

        return response


class AuthorResource(ModelResource):

    class Meta:
        queryset = Author.objects.all()
        allowed_methods = ['get']
        filtering = { "timestamp": ('gt',) }
        resource_name = 'author'
        authentication = TokenAuthentication()


    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(AuthorResource, self).build_filters(filters)
        if 'timestamp__gt' in orm_filters:
            orm_filters['timestamp__gt'] = datetime.fromtimestamp(float(filters['timestamp__gt']))
        return orm_filters


class DiseaseResource(ModelResource):

    class Meta:
        queryset = Disease.objects.all()
        allowed_methods = ['get']
        filtering = { "timestamp": ('gt',) }
        resource_name = 'disease'
        authentication = TokenAuthentication()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(DiseaseResource, self).build_filters(filters)
        if 'timestamp__gt' in orm_filters:
            orm_filters['timestamp__gt'] = datetime.fromtimestamp(float(filters['timestamp__gt']))
        return orm_filters


class HerbResource(ModelResource):
    author_id = fields.ForeignKey(AuthorResource, 'author_id')
    dehydrate_author_id = partial(foreign_key_to_id, field_name='author_id')

    class Meta:
        queryset = Herb.objects.all()
        allowed_methods = ['get']
        filtering = { "timestamp": ('gt',) }
        resource_name = 'herb'
        authentication = TokenAuthentication()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(HerbResource, self).build_filters(filters)
        if 'timestamp__gt' in orm_filters:
            orm_filters['timestamp__gt'] = datetime.fromtimestamp(float(filters['timestamp__gt']))
        return orm_filters


class HerbPictureResource(ModelResource):
    author_id = fields.ForeignKey(AuthorResource, 'author_id')
    herb_id = fields.ForeignKey(HerbResource, 'herb_id')
    dehydrate_author_id = partial(foreign_key_to_id, field_name='author_id')
    dehydrate_herb_id = partial(foreign_key_to_id, field_name='herb_id')
    screen_width = 0

    class Meta:
        queryset = HerbPicture.objects.all()
        allowed_methods = ['get']
        filtering = { "timestamp": ('gt',) }
        resource_name = 'herb-picture'
        authentication = TokenAuthentication()
        excludes = ['picture']

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(HerbPictureResource, self).build_filters(filters)
        if 'timestamp__gt' in orm_filters:
            orm_filters['timestamp__gt'] = datetime.fromtimestamp(float(filters['timestamp__gt']))
        return orm_filters

    def obj_get_list(self, request=None, **kwargs):
        token = request.GET.get('token')
        purchase = Purchase.objects.get(token=token)
        self.screen_width = purchase.screen_width
        return super(HerbPictureResource, self).obj_get_list()
    
    def dehydrate(self, bundle):
        bundle.data['url'] = "http://%s%s" % (Site.objects.get_current().domain, os.path.join(settings.MEDIA_URL, bundle.obj.url(self.screen_width)))
        return bundle





#request = None
#full_url = ''.join(['http://', get_current_site(request).domain, obj.get_absolute_url()])



class HerbUsageResource(ModelResource):
    herb_id = fields.ForeignKey(HerbResource, 'herb_id')
    disease_id = fields.ForeignKey(DiseaseResource, 'disease_id')
    dehydrate_herb_id = partial(foreign_key_to_id, field_name='herb_id')
    dehydrate_disease_id = partial(foreign_key_to_id, field_name='disease_id')

    class Meta:
        queryset = HerbUsage.objects.all()
        allowed_methods = ['get']
        filtering = { "timestamp": ('gt',) }
        resource_name = 'herb-usage'
        authentication = TokenAuthentication()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(HerbUsageResource, self).build_filters(filters)
        if 'timestamp__gt' in orm_filters:
            orm_filters['timestamp__gt'] = datetime.fromtimestamp(float(filters['timestamp__gt']))
        return orm_filters


class HerbPickResource(ModelResource):
    herb_id = fields.ForeignKey(HerbResource, 'herb_id')
    dehydrate_herb_id = partial(foreign_key_to_id, field_name='herb_id')

    class Meta:
        queryset = HerbPick.objects.all()
        allowed_methods = ['get']
        filtering = { "timestamp": ('gt',) }
        resource_name = 'herb-pick'
        authentication = TokenAuthentication()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(HerbPickResource, self).build_filters(filters)
        if 'timestamp__gt' in orm_filters:
            orm_filters['timestamp__gt'] = datetime.fromtimestamp(float(filters['timestamp__gt']))
        return orm_filters


