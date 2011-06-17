import os
import sys
import logging


# Some special mysociety preamble in order to get hold of our config
# file conf/general
package_dir = os.path.abspath(os.path.split(__file__)[0])

paths = (
    os.path.normpath(package_dir + "/../../pylib"),
    os.path.normpath(package_dir + "/../../pylib/pyc"),
    os.path.normpath(package_dir + "/../../commonlib/pylib"),
    )

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

# this is bizarely self referential but there you go
os.environ['DJANGO_SETTINGS_MODULE'] ='pyc.settings'

try:
    from config_local import config  # put settings in config_local if you're not running in a fill mysociety vhost
    SERVE_STATIC_FILES = True
except ImportError:
    SERVE_STATIC_FILES = False
    from mysociety import config
    config.set_file(os.path.abspath(package_dir + "/../../conf/general"))

# Django settings for pyc project.

if int(config.get('STAGING')):
    DEBUG = True
else:
    DEBUG = False

# configure logging
if DEBUG:
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s %(levelname)s %(message)s',
    )
else:
    logging.basicConfig(
        level = logging.WARN,
        format = '%(asctime)s %(levelname)s %(message)s',
    )

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# TODO - should we use 'django.contrib.gis.db.backends.postgis'?
DATABASE_ENGINE   = 'postgresql_psycopg2'
DATABASE_NAME     = config.get('PETITIONYOURCOUNCIL_DB_NAME')
DATABASE_USER     = config.get('PETITIONYOURCOUNCIL_DB_USER')
DATABASE_PASSWORD = config.get('PETITIONYOURCOUNCIL_DB_PASS')
DATABASE_HOST     = config.get('PETITIONYOURCOUNCIL_DB_HOST')
DATABASE_PORT     = config.get('PETITIONYOURCOUNCIL_DB_PORT')

# use this so that the test database is gis enabled
TEST_RUNNER='django.contrib.gis.tests.run_tests'

# a postGIS template, e.g.: http://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#creating-a-spatial-database-template-for-postgis
POSTGIS_TEMPLATE = 'template_postgis'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.get('DJANGO_SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'pyc.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',

    'django.contrib.admin',

    'south',
    
    'core',
)

SRID = 4326      # WGS84, the coordinate system used by the geodjango calculations 
