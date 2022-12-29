import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ADMIN_AUTH_KEY = os.environ.get('ADMIN_AUTH_KEY', 'hey-i-am-so-secret')
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGODB_HOSTNAME', 'localhost'),
        'port': int(os.environ.get('MONGODB_PORT', 27017)),
        'db': os.environ.get('MONGODB_NAME', 'Auction'),
    }
