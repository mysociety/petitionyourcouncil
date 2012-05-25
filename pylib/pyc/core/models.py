from django.contrib.gis.db import models
from django.contrib.gis.db.models import Q
from django.contrib import admin

from datetime import datetime, timedelta

import settings

class CouncilQuerySet(models.query.GeoQuerySet):
    def with_location( self ):
        """limit to having a location"""
        return self.exclude( centre__isnull=True )


class CouncilManager(models.GeoManager):
    def get_query_set(self):
        return CouncilQuerySet(self.model)

class Council(models.Model):
    slug         = models.SlugField(max_length=200, unique=True)
    name         = models.CharField(max_length=200)
    mapit_id     = models.IntegerField(unique=True)
    mapit_type   = models.CharField(max_length=3)

    petition_url = models.URLField(verify_exists=True, blank=True )
    petition_rss = models.URLField(verify_exists=True, blank=True )

    contact_email = models.EmailField( blank=True, default='' )
    
    last_checked      = models.DateTimeField(null=True)
    defer_check_until = models.DateTimeField(null=True)
    
    north_east = models.PointField(null=True)
    south_west = models.PointField(null=True)
    centre     = models.PointField(null=True)
    
    objects = CouncilManager()

    def has_location(self):
        """have bounds been set for this council"""
        if self.centre is None:
            return False
        else:
            return True
            
    def has_been_checked(self):
        """bool if the council has been checked"""
        if self.last_checked:
            return True
        else:
            return False
        

    def bump_defer_check_until(self):
        self.defer_check_until = datetime.now() + timedelta(minutes=10)
        self.save()    
        return True

    def bump_last_checked(self):
        self.last_checked = datetime.now()
        self.save()    
        return True

    @classmethod
    def missing_petitions_qs(cls):
        return (
            cls
                .objects
                .filter( petition_url='' )
                .order_by( 'last_checked', 'slug' )
        )

    @classmethod
    def missing_contacts_qs(cls):
        return (
            cls
                .objects
                .filter( contact_email='' )
                .order_by( 'last_checked', 'slug' )
        )

    @classmethod
    def need_checking_qs(cls):

        now            = datetime.now()
        checked_before = now - timedelta(days=28)

        return (
            cls
                .objects
                .filter( Q(petition_url='') | Q(contact_email='') )
                .filter( Q(last_checked__lte=checked_before) | Q(last_checked__isnull=True) )
        )

    @classmethod
    def to_check_qs(cls):

        now            = datetime.now()
        checked_before = now - timedelta(days=28)

        return (
            cls
                .need_checking_qs()
                .filter( Q(defer_check_until__lte=now)       | Q(defer_check_until__isnull=True) )
        )

    @classmethod
    def next_to_check(cls):
        """Return the next council that needs to be checked"""
        qs = cls.to_check_qs()
        try:
            return qs[0]
        except IndexError:
            return None

    def __unicode__(self):
        return self.name

    class Meta:
       ordering = ["slug"]      
     

class CouncilAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}




class Petition(models.Model):
    council     = models.ForeignKey('Council')
    
    title       = models.CharField(max_length=200)
    guid        = models.CharField(max_length=200)
    url         = models.URLField(unique=True, max_length=1000)
    description = models.CharField(max_length=2000)

    first_seen  = models.DateTimeField(auto_now_add=True)
    pub_date    = models.DateTimeField(null=True)

    def __unicode__(self):
        return "%s (%s)" % ( self.title, self.council.name )

    class Meta:
       ordering = ["-pub_date"]      
