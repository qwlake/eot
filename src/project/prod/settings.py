# settings_dev.py 로부터 재정의

from project.dev.settings import *

DEBUG = False

ALLOWED_HOSTS = [
    'resume-make.shop',
]

WSGI_APPLICATION = 'project.dev.wsgi.application'
