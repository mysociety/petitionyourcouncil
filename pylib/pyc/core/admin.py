from django.contrib import admin
from pyc.core       import models

admin.site.register(models.Council, models.CouncilAdmin)
admin.site.register(models.Petition)
