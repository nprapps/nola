#!/usr/bin/env python

"""
Project-wide application configuration.

DO NOT STORE SECRETS, PASSWORDS, ETC. IN THIS FILE.
They will be exposed to users. Use environment variables instead.
See get_secrets() below for a fast way to access them.
"""

import logging
import os

"""
NAMES
"""
# Project name to be used in urls
# Use dashes, not underscores!
PROJECT_SLUG = 'the-end-of-neighborhood-schools'

# Project name to be used in file paths
PROJECT_FILENAME = 'nola'

# The name of the repository containing the source
REPOSITORY_NAME = 'nola'
REPOSITORY_URL = 'git@github.com:nprapps/%s.git' % REPOSITORY_NAME
REPOSITORY_ALT_URL = None # 'git@bitbucket.org:nprapps/%s.git' % REPOSITORY_NAME'

# Project name used for assets rig
# Should stay the same, even if PROJECT_SLUG changes
ASSETS_SLUG = 'nola'

"""
DEPLOYMENT
"""
PRODUCTION_S3_BUCKET = 'apps.npr.org'

STAGING_S3_BUCKET = 'stage-apps.npr.org'

ASSETS_S3_BUCKET = 'assets.apps.npr.org'

DEFAULT_MAX_AGE = 20

PRODUCTION_SERVERS = ['cron.nprapps.org']
STAGING_SERVERS = ['50.112.92.131']

# Should code be deployed to the web/cron servers?
DEPLOY_TO_SERVERS = False

SERVER_USER = 'ubuntu'
SERVER_PYTHON = 'python2.7'
SERVER_PROJECT_PATH = '/home/%s/apps/%s' % (SERVER_USER, PROJECT_FILENAME)
SERVER_REPOSITORY_PATH = '%s/repository' % SERVER_PROJECT_PATH
SERVER_VIRTUALENV_PATH = '%s/virtualenv' % SERVER_PROJECT_PATH

# Should the crontab file be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_CRONTAB = False

# Should the service configurations be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_SERVICES = False

UWSGI_SOCKET_PATH = '/tmp/%s.uwsgi.sock' % PROJECT_FILENAME
UWSGI_LOG_PATH = '/var/log/%s.uwsgi.log' % PROJECT_FILENAME
APP_LOG_PATH = '/var/log/%s.app.log' % PROJECT_FILENAME

# Services are the server-side services we want to enable and configure.
# A three-tuple following this format:
# (service name, service deployment path, service config file extension)
SERVER_SERVICES = [
    ('app', SERVER_REPOSITORY_PATH, 'ini'),
    ('uwsgi', '/etc/init', 'conf'),
    ('nginx', '/etc/nginx/locations-enabled', 'conf'),
]

# These variables will be set at runtime. See configure_targets() below
S3_BUCKETS = []
S3_BASE_URL = ''
SERVERS = []
SERVER_BASE_URL = ''
DEBUG = True

"""
Logging
"""
LOG_FORMAT = '%(levelname)s:%(name)s:%(asctime)s: %(message)s'

"""
COPY EDITING
"""
COPY_GOOGLE_DOC_URL = 'https://docs.google.com/a/tylerjfisher.com/spreadsheet/ccc?key=0AqjLQISCZzBkdGFRcnF1aWlyTjJQUnpPbFl6eDJmQmc'
COPY_PATH = 'data/copy.xlsx'

"""
SHARING
"""
SHARE_URL = 'http://%s/%s/' % (PRODUCTION_S3_BUCKET, PROJECT_SLUG)

"""
ADS
"""

NPR_DFP = {
    'STORY_ID': '1002',
    'TARGET': 'homepage',
    'ENVIRONMENT': 'NPRTEST',
    'TESTSERVER': 'false'
}

"""
SERVICES
"""
GOOGLE_ANALYTICS = {
    'ACCOUNT_ID': 'UA-5828686-4',
    'DOMAIN': PRODUCTION_S3_BUCKET,
    'TOPICS': '[1013,1049,1019,1003,1001]' # e.g. '[1014,3,1003,1002,1001]'
}

DISQUS_UUID = 'f9796633-27cb-11e4-b359-a820662c8a94'

"""
Utilities
"""
def get_secrets():
    """
    A method for accessing our secrets.
    """
    secrets = [
        'TWITTER_API_CONSUMER_KEY',
        'TWITTER_API_CONSUMER_SECRET',
        'TWITTER_API_OAUTH_TOKEN',
        'TWITTER_API_OAUTH_SECRET',
        'FACEBOOK_API_APP_TOKEN'
    ]

    secrets_dict = {}

    for secret in secrets:
        name = '%s_%s' % (PROJECT_FILENAME, secret)
        secrets_dict[secret] = os.environ.get(name, None)

    return secrets_dict

def configure_targets(deployment_target):
    """
    Configure deployment targets. Abstracted so this can be
    overriden for rendering before deployment.
    """
    global S3_BUCKET
    global S3_BASE_URL
    global SERVERS
    global SERVER_BASE_URL
    global DEBUG
    global DEPLOYMENT_TARGET
    global APP_LOG_PATH
    global DISQUS_SHORTNAME
    global LOG_LEVEL
    global ASSETS_MAX_AGE


    if deployment_target == 'production':
        S3_BUCKET = PRODUCTION_S3_BUCKET
        S3_BASE_URL = 'http://%s/%s' % (S3_BUCKET, PROJECT_SLUG)
        SERVERS = PRODUCTION_SERVERS
        SERVER_BASE_URL = 'http://%s/%s' % (SERVERS[0], PROJECT_SLUG)
        DISQUS_SHORTNAME = 'npr-news'
        LOG_LEVEL = logging.WARNING
        DEBUG = False
        ASSETS_MAX_AGE = 86400
    elif deployment_target == 'staging':
        S3_BUCKET = STAGING_S3_BUCKET
        S3_BASE_URL = 'http://%s/%s' % (S3_BUCKET, PROJECT_SLUG)
        SERVERS = STAGING_SERVERS
        SERVER_BASE_URL = 'http://%s/%s' % (SERVERS[0], PROJECT_SLUG)
        DISQUS_SHORTNAME = 'nprviz-test'
        LOG_LEVEL = logging.DEBUG
        DEBUG = True
        ASSETS_MAX_AGE = 20
    else:
        S3_BUCKET = ''
        S3_BASE_URL = 'http://127.0.0.1:8000'
        SERVERS = []
        SERVER_BASE_URL = 'http://127.0.0.1:8001/%s' % PROJECT_SLUG
        DISQUS_SHORTNAME = 'nprviz-test'
        DEBUG = True
        APP_LOG_PATH = '/tmp/%s.app.log' % PROJECT_SLUG
        LOG_LEVEL = logging.DEBUG
        ASSETS_MAX_AGE = 20

    DEPLOYMENT_TARGET = deployment_target

"""
Run automated configuration
"""
DEPLOYMENT_TARGET = os.environ.get('DEPLOYMENT_TARGET', None)

configure_targets(DEPLOYMENT_TARGET)

