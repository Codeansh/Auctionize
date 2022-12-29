import os, json, jwt
from werkzeug.wrappers import Request, Response
from app.auth.models import User
from bson import ObjectId

class Authentication_Middleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.environ.get('REQUEST_URI') in os.environ.get('UNAUTHENTICATED_ROUTES',['/auth/signup','/auth/login']):
            return self.app(environ, start_response)

        secret = request.headers.get('ADMIN_AUTH','')
        if secret == os.environ.get('ADMIN_AUTH_KEY'):
            environ['is_admin'] = True
            return self.app(environ, start_response)
        
        token = None
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            error = {'message' : 'Please Enter the token to verify your identity '}
            response = Response(json.dumps(error), mimetype='text/plain', status=401)
            return response(environ, start_response)

        try:
            user_id = jwt.decode(token, os.environ.get('SECRET_KEY','this is a secret key'), 'HS256')['user_id']
            if not user_id:
                error = {'message': 'Please Login again'}

                response = Response(json.dumps(error), mimetype='text/plain', status=401)
                return response(environ, start_response)

        except Exception as e:
            error = {'message': 'Something went wrong ' + str(e)}
            response = Response(json.dumps(error), mimetype='text/plain', status=401)
            return response(environ, start_response)

        user_obj = User.objects(id=ObjectId(user_id))

        if not user_obj:
            error = {'message' : 'user_id not found'}
            response = Response(json.dumps(error), mimetype='text/plain', status=401)
            return response(environ, start_response)

        environ['user_id'] = user_id
        return self.app(environ, start_response)
