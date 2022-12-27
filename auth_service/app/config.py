import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ADMIN_AUTH_KEY = os.environ.get('ADMIN_AUTH_SECRET', 'hey-i-am-so-secret')
    MONGODB_SETTINGS = {
        "host": f"mongodb://{ os.environ.get('MONGODB_HOSTNAME', 'localhost')}:27017",
        "port": int(os.environ.get('MONGODB_PORT', 27017)),
        "db": os.environ.get('MONGODB_NAME', 'Auth')
    }
    UNAUTHENTICATED_ROUTES = os.environ.get('UNAUTHENTICATED_ROUTES')
