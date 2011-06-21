from django.conf.urls.defaults import *
from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('pyc.core.views',
    (r'^$',        'index'  ),
    (r'^search/$', 'search' ),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)

# server static files if needed
if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (   r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT }
        ),
    )