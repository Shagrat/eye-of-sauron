import os
from flask import json
from api.restplus import api
from app import wsgi


with wsgi.test_request_context():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', 'swagger.json'), 'w') as stream:
         stream.write(json.dumps(api.__schema__))
