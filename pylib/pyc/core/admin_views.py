import logging

from django.shortcuts  import render_to_response, get_object_or_404, redirect
from django.template   import RequestContext
from django.views.generic.list_detail   import object_list, object_detail
from django.contrib.admin.views.decorators import staff_member_required

from pyc.core.models import Council

from helpers import postcode_to_council_ids

# Aim: go through all the councils that have no petition_url and that have
# not been checked recently or at all. Use the defer_check_until field to
# reduce the chance that two people work on the same council.

# There are pages that:
#   * lists all councils that need to be checked.
#   * lets you edit one in particular.
#   * sends you to the next council that needs checking.

@staff_member_required
def list_missing_sites(request):
    """Go through councils that need to be checked"""

    return object_list(
        request,
        queryset=Council.missing_petitons_qs(),
        template_name='core/admin/list_missing_sites.html',
    )

@staff_member_required
def next_missing_site( request ):
    """Redirect to the next missing site, or back to list page"""

    council = Council.next_to_check()
    
    if council:
        return redirect( do_missing_site, council_id=council.id )
    else:
        return redirect( list_missing_sites )

@staff_member_required
def do_missing_site( request, council_id ):
    """Go through councils that need to be checked"""

    return render_to_response(
        'core/admin/do_missing_site.html',
        {},
        context_instance=RequestContext(request)
    )

