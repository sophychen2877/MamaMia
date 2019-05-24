#SECRET_KEY and database with password connection (and any other API keys) need to be kept in the instance file, which is not subject to version control
#these configuration settings are used in dev environment
SECRET_KEY = ''

import os
POSTGRES_DATABASE = os.environ['POSTGRES_DATABASE']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']


#use postgresql
SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = os.environ['DEBUG']
