from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template

import settings

admin.autodiscover()

urlpatterns = patterns('pyc.core.views',
    (r'^$',                          'index'   ),
    (r'^search/$',                   'search'  ),
    (r'^council/(?P<slug>.*?)/$',    'council' ),
    (r'^petition/next.json$',        'petition_next' ),
    (r'^report_error/$',             'report_error' ),

    (r'^out/(?P<slug>.*?)/(?P<petition_id>\d+)/$', 'out' ),
    (r'^out/(?P<slug>.*?)/$',                      'out' ),

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

# static docs that get templated
urlpatterns += patterns('',
    (r'^about$', direct_to_template, {'template': 'about.html'}),
    (r'^privacy$', direct_to_template, {'template': 'privacy.html'}),
)