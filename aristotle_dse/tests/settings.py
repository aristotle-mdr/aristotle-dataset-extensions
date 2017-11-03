import os, sys
from aristotle_mdr.tests.settings.settings import *
from aristotle_mdr.required_settings import INSTALLED_APPS

INSTALLED_APPS = (
    # The good stuff
    'aristotle_dse',
) + INSTALLED_APPS

ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] = ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] +['aristotle_dse']

ROOT_URLCONF = 'aristotle_dse.tests.urls'