import os, sys
from aristotle_mdr.tests.settings.settings import *

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

ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] = ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] +['aristotle_dse']

ROOT_URLCONF = 'aristotle_dse.tests.urls'