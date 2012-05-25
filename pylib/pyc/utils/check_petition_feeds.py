#!/usr/bin/env python

import re
import logging
import httplib2
import sys
import feedparser
import pprint
import dateutil.parser
import os

sys.path.append('../..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pyc.settings'

pprinter = pprint.PrettyPrinter(indent=4)

from pyc import settings
from pyc.core.models import Council, Petition

councils_with_rss = Council.objects.exclude( petition_rss='' )

for council in councils_with_rss:

    logging.debug( "%s (%s)" % (council.name, council.petition_rss) )

    rss_data = feedparser.parse( council.petition_rss )
    rss_entries = rss_data['entries']

    for rss_entry in rss_entries:

        # pprinter.pprint( rss_entry )

        pub_date = dateutil.parser.parse( rss_entry['updated'], fuzzy=True )

        # we need something to act as an identifier, so go through list until we
        # find one.
        guid = rss_entry.get('id') or rss_entry.get('link')
            
        petition, created = Petition.objects.get_or_create(
            guid   = guid,
            defaults = {
                'council'     : council,
                'title'       : rss_entry['title'][:190],
                'url'         : rss_entry['link'],
                'description' : rss_entry['summary'][:1900],  # see note below
                'pub_date'    : pub_date,
            },
        )

        # Note on the 190/1900 cap.
        #
        # The title and description database fields can store 200 or 2000 chars,
        # but the encoding is SQL so it is actually 2000 bytes. Hence any entry
        # containing wide characters that gets truncated may be 200(0) chars, 
        # but > 200(0) bytes causing the insert query to fail.
        #
        #   django.db.utils.DatabaseError: value too long for type character varying(2000)
        #
        # We should switch the encoding to utf8, or do some smarter truncating.
        # But for now just trimming off more than we need to does the trick.
