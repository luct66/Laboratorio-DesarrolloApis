from .settings import *

SECRET_KEY = 'CHANGEME!!!'
DEBUG = False

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'desarrolloapi',
'USER': 'postgres',
'PASSWORD': 'homero74',
}
}
