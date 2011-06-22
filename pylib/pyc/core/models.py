from django.contrib.gis.db import models
from django.contrib import admin

from datetime import datetime, timedelta

import settings

class Council(models.Model):
    slug         = models.SlugField(max_length=200, unique=True)
    name         = models.CharField(max_length=200)
    mapit_id     = models.IntegerField(unique=True)
    mapit_type   = models.CharField(max_length=3)
    petition_url = models.URLField(verify_exists=False, blank=True )
    petition_rss = models.URLField(verify_exists=False, blank=True )
    
    last_checked      = models.DateTimeField(null=True)
    defer_check_until = models.DateTimeField(null=True)

    @classmethod
    def missing_petitons(cls):
        # checked_before = datetime.now() - timedelta(days=28)
        return (
            cls
                .objects
                .filter( petition_url='' )
                # .filter( last_checked__lte=checked_before )
                .order_by( 'last_checked', 'slug' )
        )
    
    # @classmethod
    # def need_checking(cls):
    #     checked_before = datetime.now() - timedelta(days=28)
    #     return (
    #         cls
    #             .objects
    #             .filter( petition_url='' )
    #             .filter( last_checked__lte=checked_before )
    #             .order_by( 'last_checked', 'slug' )
    #     )

    def __unicode__(self):
        return self.name

    class Meta:
       ordering = ["slug"]      
     

class CouncilAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

