"""
Provides one endpoint to API class containing namespaces
for endpoints
"""
from flask_restplus import Api


api = Api(version='0.1', title='Sleepless API',
          description='Site monitoring tool for test assigment')
