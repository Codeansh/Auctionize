import os
from werkzeug.wrappers import Request, Response
import json
import requests


class AuthenticationMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        secret = request.headers.get('ADMIN_AUTH', '')

        if secret == os.environ.get('ADMIN_AUTH_KEY'):
            environ['is_admin'] = True
            return self.app(environ, start_response)

        token = request.headers.get("Authorization", "")

        if not token:
            error = {"message": "Missing or Invalid token"}
            response = Response(json.dumps(error), mimetype='application/json', status=401)
            return response(environ, start_response)
        try:
            response = requests.post(
                f"http://{os.environ.get('AUTH_HOSTNAME','localhost')}:5000/auth/validate",
                headers={'Authorization': token}
            )
        except ConnectionError as e:
            error = {"message": e}
            response = Response(json.dumps(error), mimetype='application/json', status=401)
            return response(environ, start_response)

        if response.status_code != 200:
            response = Response(response.text, mimetype='application/json', status=401)
            return response(environ, start_response)


        user_id = json.loads(response.text).get('user_id')
        environ['user_id'] = user_id

        return self.app(environ, start_response)
