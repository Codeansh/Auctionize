from flask import Flask
from app.config import Config
from flask_mongoengine import MongoEngine
from app.auth_middleware import AuthenticationMiddleware
import os
print("connectiong to db ")
print(os.environ.get('MONGODB_HOSTNAME'))
db = MongoEngine()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.wsgi_app = AuthenticationMiddleware(app.wsgi_app)
    db.init_app(app)
    from app.auction.routes import auction
    app.register_blueprint(auction)

    return app
