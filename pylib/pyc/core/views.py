import logging

from django.shortcuts  import render_to_response, get_object_or_404, redirect
from django.template   import RequestContext
from django.views.generic.list_detail   import object_list, object_detail

from pyc.core import models

from helpers import postcode_to_council_ids

def index(request):
    """Homepage"""
    return render_to_response(
        'core/index.html',
        {},
        context_instance=RequestContext(request)
    )



def search(request):
    """Search for postcode (initially - may extend later)"""

    q = request.GET.get('q', '')
    if not q:
        return redirect(index)

    # assume that the query is a postcode and search for it
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

    # If we've only found one result then go straight there
    if qs.count() == 1:
        return redirect( council, slug=qs[0].slug )
        
    return object_list(
        request,
        queryset      = qs,
        template_name = 'core/search.html',
        extra_context = { "q": q, },
    )


def council(request, slug):
    """Show results for a single council"""

    try:
        council = models.Council.objects.get(slug=slug)
    except models.Council.DoesNotExist:
        raise Http404

    return render_to_response(
        'core/council.html',
        {
            'council': council,
        },
        context_instance=RequestContext(request)
    )
