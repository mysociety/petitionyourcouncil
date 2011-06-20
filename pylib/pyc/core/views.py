from django.shortcuts  import render_to_response, get_object_or_404
from django.template   import RequestContext


def index(request, q=''):
    """Homepage"""
    return render_to_response(
        'core/index.html',
        {},
        context_instance=RequestContext(request)
    )



def search(request, q=''):
    """Search for postcode (initially - may extend later)"""
    return render_to_response(
        'core/search.html',
        {
            "q": q,
        },
        context_instance=RequestContext(request)
    )