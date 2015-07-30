import os, sys
from aristotle_mdr.required_settings import *
BASE = os.path.dirname(os.path.dirname(__file__))

sys.path.insert(1,BASE)
sys.path.insert(1,os.path.join(BASE, "tests"))

SECRET_KEY = 'inara+vtkprm7@0(fsc$+grbz9-s+tmo9d)e#k(9uf8m281&$7xhdkjr'
SOUTH_TESTS_MIGRATE = True

MEDIA_ROOT = os.path.join(BASE, "media")

MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = 'uploads/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
   }
}

class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES = DisableMigrations()

INSTALLED_APPS = (
    #The good stuff
    'aristotle_dse',
) + INSTALLED_APPS

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE, 'aristotle_mdr/tests/whoosh_index'),
        'INCLUDE_SPELLING':True,
    },
}

# https://docs.djangoproject.com/en/1.6/topics/testing/overview/#speeding-up-the-tests
# We do a lot of user log in testing, this should speed stuff up.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] = ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] +['aristotle_dse']

ROOT_URLCONF = 'aristotle_dse.tests.urls'