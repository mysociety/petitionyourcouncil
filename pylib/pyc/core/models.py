from django.contrib.gis.db import models
from django.contrib import admin

import settings

class Council(models.Model):
    slug         = models.SlugField(max_length=200, unique=True)
    name         = models.CharField(max_length=200)
    mapit_id     = models.IntegerField(unique=True)
    mapit_type   = models.CharField(max_length=3)
    petition_url = models.URLField(verify_exists=False, blank=False)
    petition_rss = models.URLField(verify_exists=False, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
       ordering = ["slug"]

class CouncilAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Council, CouncilAdmin)
