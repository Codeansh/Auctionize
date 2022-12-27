from flask import Flask, jsonify
from app.config import Config
from flask_mongoengine import MongoEngine
from app.auth_middleware import Authentication_Middleware
import os

print("connectiong to db ")
print(os.environ.get('MONGODB_HOSTNAME'))
db = MongoEngine()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.wsgi_app = Authentication_Middleware(app.wsgi_app)
    from app.auth.routes import auth
    app.register_blueprint(auth)
    
    return app

