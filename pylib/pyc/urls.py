from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('pyc.core.views',
    (r'^$',        'index'  ),
    (r'^search/$', 'search' ),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)
