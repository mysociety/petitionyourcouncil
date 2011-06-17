from django.contrib.gis.db import models
from django.contrib import admin

import settings

class Council(models.Model):
    slug         = models.SlugField(max_length=200, unique=True)
    name         = models.CharField(max_length=200)
    petition_url = models.URLField(verify_exists=False)
    petition_rss = models.URLField(verify_exists=False)

    def __unicode__(self):
        return self.name

class CouncilAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Council, CouncilAdmin)
