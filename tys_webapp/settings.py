import os

CONSUMER_KEY = os.environ['TYS_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TYS_CONSUMER_SECRET']


OAUTH_SCOPE = ['email_r', 'transactions_r', 'cart_rw']
SCOPE_URL_EXT = '?scope=' + '%20'.join(OAUTH_SCOPE)
