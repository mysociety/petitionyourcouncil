import re
import logging
import httplib2
import sys
import feedparser
import pprint
import dateutil.parser

pprinter = pprint.PrettyPrinter(indent=4)

sys.path.append('..')

from pyc import settings
from pyc.core.models import Council, Petition

councils_with_rss = Council.objects.exclude( petition_rss='' )

for council in councils_with_rss:
    print council.name

    logging.debug( "%s (%s)" % (council.name, council.petition_rss) )

    rss_data = feedparser.parse( council.petition_rss )
    rss_entries = rss_data['entries']

    for rss_entry in rss_entries:

        # pprinter.pprint( rss_entry )

        pub_date = dateutil.parser.parse( rss_entry['updated'], fuzzy=True )
            
        petition = Petition.objects.get_or_create(
            guid   = rss_entry['id'],
            defaults = {
                'council'     : council,
                'title'       : rss_entry['title'],
                'url'         : rss_entry['link'],
                'description' : rss_entry['summary'],
                'pub_date'    : pub_date,
            },
        )
