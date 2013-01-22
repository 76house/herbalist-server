# Create your views here.

#from herbapp.models import Author
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404  


# home page
def index(request, template = 'index.html'):

    # static page

    return render_to_response(template, {
        }, context_instance=RequestContext(request))

