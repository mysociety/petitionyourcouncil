import urllib2
import simplejson as json
import logging

from django.contrib.gis.geos import point

import settings

def lat_lng_to_point( lat, lng):
    return point.Point(float(lng), float(lat), srid=settings.SRID)

def postcode_to_point( postcode ):
    # get postcode from Mapit
    try:
        url = settings.MAPIT_URL + 'postcode/' + urllib2.quote(postcode)
        res = urllib2.urlopen( url )
        mapit_response = json.load( res )
    except urllib2.HTTPError:
        return None

    code = mapit_response.get('code')
    if code == 404 or code == 400:
        return None

    latitude  = mapit_response['wgs84_lat']
    longitude = mapit_response['wgs84_lon']

    return lat_lng_to_point( latitude, longitude )


def postcode_to_council_ids( postcode ):

    if not postcode:
        return None

    # get postcode from Mapit
    try:
        url = settings.MAPIT_URL + 'postcode/' + urllib2.quote(postcode)
        res = urllib2.urlopen( url )
        mapit_response = json.load( res )
    except urllib2.HTTPError:
        return None

    code = mapit_response.get('code')
    if code == 404 or code == 400:
        return None

    shortcuts = mapit_response['shortcuts']
    # logging.debug( shortcuts )

    # extract councils - return value may be one of:
    #   SA19 8BA: { ..., 'council': 2604 }
    #   GL50 2PR: {..., 'council': {'county': 2226, 'district': 2326} }    
    try:
        council_ids = shortcuts['council'].values()
    except AttributeError:
        council_ids = [ shortcuts['council'] ]

    # logging.debug( council_ids )

    return council_ids
