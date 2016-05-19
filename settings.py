# coding: utf8

import os

ENV = os.getenv('HTGW_ENV')

if ENV == 'PROD':
    from settings_prod import *
if ENV == 'TEST':
    from settings_test import *
else:
    from settings_dev import *
