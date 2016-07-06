# coding: utf8

import os

ENV = os.getenv('HTAPP_ENV')

if ENV == 'PROD':
    from settings_prod import *
elif ENV == 'TEST':
    from settings_test import *
else:
    from settings_dev import *
