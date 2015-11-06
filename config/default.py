# -*- coding: utf-8 -*-
""" Configurações default
"""
__author__ = 'rangel.torrezan'

SQLALCHEMY_DATABASE_URI = 'oracle://HIVE_AKIRA:JF0s8aq@oradev.nexxera.com/dev'
SQLALCHEMY_POOL_SIZE = None
SQLALCHEMY_POOL_TIMEOUT = None
SQLALCHEMY_POOL_RECYCLE = None
DEBUG = True

CELERY_BROKER_URL = 'redis://xxx/0'

MAIL_DEFAULT_SENDER = 'hive@nexxera.com'
MAIL_SERVER = 'smtp.xxx.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'