import logging
import re

from django.shortcuts  import render_to_response, get_object_or_404, redirect
from django.template   import RequestContext
from django.views.generic.list_detail   import object_list, object_detail
from django import http
from django.utils import simplejson
from django.core.mail import send_mail
from django.core.urlresolvers import  reverse

from pyc.core import models

from helpers import postcode_to_council_ids
import settings

def index(request):
    """Homepage"""
    return render_to_response(
        'core/index.html',
        {},
        context_instance=RequestContext(request)
    )


def search(request):
    """Search for postcode or a council name"""

    q = request.GET.get('q', '')
    if not q:
        return redirect(index)

    # assume that the query is a postcode if it has a number in
    if re.search( r'\d', q ):
        council_ids = postcode_to_council_ids( q )
    else:
        # slightly inefficient - but keeps code cleaner later on
        matches = models.Council.objects.filter( name__icontains=q )
        council_ids = [ i.mapit_id for i in matches ]

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
    result_count = qs.count()
    if result_count == 1:
        return redirect( council, slug=qs[0].slug )
    
    # have more than one result - work out the bounds for the first five
    if result_count > 1:
        to_display = qs.with_location()[:5]
        bounds = {
            "north": max( [ i.north_east.x for i in to_display ]),
            "east":  max( [ i.north_east.y for i in to_display ]),
            "south": min( [ i.south_west.x for i in to_display ]),
            "west":  min( [ i.south_west.y for i in to_display ]),
        }
        kml_ids = [ i.mapit_id for i in to_display ]
        types = [ i.mapit_type for i in to_display ]
        two_tier = True if 'DIS' in types or 'CTY' in types else False
    else:
        bounds = None
        kml_ids = []
        two_tier = False

    return object_list(
        request,
        queryset      = qs,
        template_name = 'core/search.html',
        extra_context = {
            "q":       q,
            "bounds":  bounds,
            "kml_ids": kml_ids,
            "two_tier": two_tier,
        },
    )


def council(request, slug):
    """Show results for a single council"""

    try:
        council = models.Council.objects.get(slug=slug)
    except models.Council.DoesNotExist:
        raise http.Http404

    return render_to_response(
        'core/council.html',
        {
            'council': council,
        },
        context_instance=RequestContext(request)
    )


def out(request, slug, petition_id=None ):
    """Show results for a single council"""

    try:
        council = models.Council.objects.get(slug=slug)
    except models.Council.DoesNotExist:
        raise http.Http404

    if petition_id:
        try:
            petition = council.petition_set.get(id=petition_id)
        except models.Petition.DoesNotExist:
            raise http.Http404
    else:
        petition = None

    if petition:
        out_url = petition.url
    elif council.petition_url:
        out_url = council.petition_url
    else:
        # No URL found - handle this by sending to the council page
        return redirect( council, slug=slug )

    return render_to_response(
        'core/out.html',
        {
            'council': council,
            'out_url': out_url,
        },
        context_instance=RequestContext(request)
    )


def petition_next (request):
    """Return json of the next petition"""
    last_id = int( request.GET.get('last_id', 0 ) )
    
    qs = models.Petition.objects.order_by( '-pub_date' )

    if last_id:
        # select the next most recent petition that has a location but is not
        # from the same council as the last one
        last_petition = get_object_or_404( models.Petition, pk=last_id)

        # TODO - would prefer not to use the council__centre__is_null here and 
        # to use the 'with_location' queryset instead but that was causing a
        # 'ProgrammingError' exception on fury with D1.1

        qs = (
            qs
              .filter( council__centre__isnull=False )
              .filter( pub_date__lt=last_petition.pub_date )
              .exclude( council=last_petition.council )
        )

    try:
        petition = qs[0]
    except IndexError:
        raise http.Http404

    data = {
        "id":          petition.id,
        "title":       petition.title,    
        "lat":         petition.council.centre.x,
        "lon":         petition.council.centre.y,
        "council":     petition.council.name,
        "council_url": reverse( council, kwargs={'slug':petition.council.slug} ),
    }
    
    response = http.HttpResponse(content_type='application/json; charset=utf-8')
    simplejson.dump(data, response, ensure_ascii=False, indent=4)
    return response


def report_error(request):
    """Let users report an error on any page. Email it to ourselves"""

    url     = request.REQUEST.get('url',     '')
    message = request.REQUEST.get('message', '')
    email   = request.REQUEST.get('email',   '')
    message_sent = False
    
    if request.method == 'POST' and message:
        send_mail(
            "[PetitionYourCouncil] Error reported on '%s'" % url,
            "url: %s\nemail: %s\n\n%s" % (url, email, message),
            settings.REPORT_ERRORS_FROM_EMAIL_ADDRESS,
            [ settings.REPORT_ERRORS_TO_EMAIL_ADDRESS ],
            fail_silently=False
        )
        message_sent = True        
    
    return render_to_response(
        'core/report_error.html',
        {
            'url':          url,
            'message':      message,
            'email':        email,
            'message_sent': message_sent,
        },
        context_instance=RequestContext(request)
    )
