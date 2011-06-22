from django.conf.urls.defaults import *
from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('pyc.core.views',
    (r'^$',                          'index'   ),
    (r'^search/$',                   'search'  ),
    (r'^council/(?P<slug>.*?)/$',    'council' ),
)

urlpatterns += patterns('pyc.core.admin_views',
    (r'^admin/core/find_missing_sites/next/',                'next_missing_site'  ),
    (r'^admin/core/find_missing_sites/(?P<council_id>\d+)/', 'do_missing_site'    ),
    (r'^admin/core/find_missing_sites/',                     'list_missing_sites' ),
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