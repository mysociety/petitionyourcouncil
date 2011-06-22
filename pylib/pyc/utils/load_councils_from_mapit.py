import re
import logging
import httplib2
import sys

try:
    import json
except ImportError:
    import simplejson as json 

sys.path.append('..')

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
    logging.debug( "Looking at %s (%s)" % ( id, str(entry) ) )


    name = entry['name']
    slug = re.sub( '[^a-z]+', '-', name.lower() )

    council = Council.objects.get_or_create(
        mapit_id   = id,
        defaults = {
            'slug'       : slug,
            'name'       : name,
            'mapit_type' : entry['type'],
        },
    )

