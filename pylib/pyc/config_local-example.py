config = dict(
    PETITIONYOURCOUNCIL_DB_NAME = 'petitionyourcouncil',         # Name of your postgres database
    PETITIONYOURCOUNCIL_DB_USER = '',            # Postgres user to connect with
    PETITIONYOURCOUNCIL_DB_PASS = '',            # Password for postgres
    PETITIONYOURCOUNCIL_DB_HOST = 'localhost',   # host for postgres
    PETITIONYOURCOUNCIL_DB_PORT = 5432,          # port for postgres
    
    # Probably doesn't need changing.
    MAPIT_URL = 'http://mapit.mysociety.org/',
    
    # Set this to some random stuff yourself
    DJANGO_SECRET_KEY = 'FIXME',

    STAGING = '1',

    GOOGLE_ANALYTICS_ACCOUNT_LIVE  = 'UA-24118464-1',
    GOOGLE_ANALYTICS_ACCOUNT_STAGE = 'UA-24118464-2',
)
