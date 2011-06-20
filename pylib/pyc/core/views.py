import logging

from django.shortcuts  import render_to_response, get_object_or_404
from django.template   import RequestContext
from django.views.generic.list_detail   import object_list, object_detail

from pyc.core import models

from helpers import postcode_to_council_ids

def index(request, q=''):
    """Homepage"""
    return render_to_response(
        'core/index.html',
        {},
        context_instance=RequestContext(request)
    )



def search(request):
    """Search for postcode (initially - may extend later)"""

    # assume that the query is a postcode and search for it
    q = request.GET.get('q', '')
    council_ids = postcode_to_council_ids( q )

    if not council_ids:
        return render_to_response(
            'core/search.html',
            { "q": q, },
            context_instance=RequestContext(request)
        )
    
    # output is a list of councils that cover that postcode
    qs = models.Council.objects.filter( mapit_id__in=council_ids )

    # check that all the councils are found - may not have all loaded into db
    if qs.count() != len( council_ids ):
        council_id_list = str.join( ', ', [ str(i) for i in council_ids] )
        logging.error(
            "Could not load some councils from db for pc '%s': %s" % ( q, council_id_list )
        )


    return object_list(
        request,
        queryset      = qs,
        template_name = 'core/search.html',
        extra_context = { "q": q, },
    )