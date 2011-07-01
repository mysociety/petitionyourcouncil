#!/usr/bin/env python

import re
import logging
import httplib2
import sys
import time


try:
    import json
except ImportError:
    import simplejson as json 

sys.path.append('..')

from django.contrib.gis.geos import Point

from pyc import settings
from pyc.core.models import Council

    
# full list of codes under 'Multiple Areas' heading http://mapit.mysociety.org/:
# chosen are from mySociety::VotingArea::council_parent_types
mapit_areas_url = 'http://mapit.mysociety.org/areas/DIS,LBO,MTD,UTA,LGD,CTY,COI.json'

h = httplib2.Http(cache='.cache')

logging.debug( "Fetching " + mapit_areas_url )
response, content = h.request( mapit_areas_url )
data = json.loads(content)

for id in data:
    entry = data[id]

    logging.debug( "Looking at %s (%s)" % ( id, str(entry['name']) ) )
    # logging.debug( entry )

    name = entry['name']
    slug = re.sub( '[^a-z]+', '-', name.lower() )

    council, created = Council.objects.get_or_create(
        mapit_id   = id,
        defaults = {
            'slug'       : slug,
            'name'       : name,
            'mapit_type' : entry['type'],
        },
    )

    if not council.has_location():
        
        geometry_url = "http://mapit.mysociety.org/area/%s/geometry" % council.mapit_id

        logging.debug( "  Fetching geometry for %s" % ( council.name ) )

        response, content = h.request( geometry_url )
        geometry = json.loads(content)

        if 'error' in geometry:
            logging.warn( "  Error for %s (%s): %s" % ( council.name, geometry_url, geometry['error'] ) )
        else:
            council.north_east = Point( geometry['max_lat'], geometry['max_lon'] )
            council.south_west = Point( geometry['min_lat'], geometry['min_lon'] )
            council.centre = Point( geometry['centre_lat'], geometry['centre_lon'] )
            council.save()

        # don't hit mapit's rate limiter on my machine
        time.sleep( 4 )
