"""
Django production settings for librarycloud project.
"""

import os
import dj_database_url

from .base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['protected-harbor-5387.herokuapp.com',
				 'intersectional-librarycloud.herokuapp.com']

# Parse database configuration from $DATABASE_URL
DATABASES['default'] =  dj_database_url.config()

# Enable Connection Pooling (if desired)
DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
