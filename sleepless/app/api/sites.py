"""
Contains endpoints for API
"""
import time
import datetime
import requests
from flask import request
from flask_restplus import Resource, fields
from werkzeug.exceptions import BadRequest
from app.api.restplus import api
from app.api.io_logic import get_sites_from_io, update_sites_in_io


ns_sites = api.namespace('sites', description='Operations with sites')
ns_monitoring = api.namespace('monitoring', description='Monitoring operations')


site = api.model('Site', {
    'url': fields.String(required=True, description='URL')
})

site_update = api.model('Site to update', {
    'url': fields.String(required=True, description='URL'),
    'new_url': fields.String(required=True, description='URL'),
})

site_status = api.model('Site to monitor', {
    'url': fields.String(required=True, description='URL'),
    'last_status': fields.String(description='Last known status'),
    'last_checked': fields.DateTime(description='Last update'),
})


def test_sites():
    """
    Test sites availability and returns List of sites objects
    :return: List of sites objects
    """
    sites = get_sites_from_io().items()
    for _key, domain in sites:
        start = time.time()
        try:
            test_request = requests.get(domain.get('url'), timeout=2)
        except requests.exceptions.MissingSchema:
            domain['last_status'] = 'No schema supplied'
            continue
        except requests.exceptions.ConnectionError:
            domain['last_status'] = 'Connection Error'
            continue
        except Exception:
            domain['last_status'] = 'Error'
            continue
        elapsed = time.time() - start
        if test_request.status_code == requests.codes.ok and elapsed <= 0.25:
            domain['last_status'] = 'OK'
        elif test_request.status_code == requests.codes.ok:
            domain['last_status'] = 'Slow'
        else:
            domain['last_status'] = 'Error'
        domain['last_checked'] = datetime.datetime.fromtimestamp(start)
        return sites


@ns_sites.route('/')
class SitesCollection(Resource):
    """
    Contains endpoints for listing, adding, deleting and updating sites objects
    """
    @staticmethod
    @api.marshal_list_with(site)
    def get():
        """
        Returns list of sites.
        """
        return [v for k, v in get_sites_from_io().items()]

    @staticmethod
    @api.response(201, 'URL successfully added.')
    @api.expect(site)
    def post():
        """
        Adds new site to monitor.
        * Send a JSON object with the URL in request body.
        ```
        {
          "url": "New URL"
        }
        ```
        Returns list of sites.
        """
        data = request.json
        if not data.get('url'):
            raise BadRequest
        sites = update_sites_in_io(data.get('url'))
        return [v for k, v in sites.items()], 201

    @staticmethod
    @api.expect(site_update)
    @api.response(204, 'Site successfully updated.')
    def put():
        """
        Updates site url.
        * Send a JSON object with the new and old URL in request body.
        ```
        {
          "url": "Current URL",
          "new_url": "New URL"
        }
        ```
        Returns list of sites.
        """
        data = request.json
        if not data.get('url') or not data.get('new_url'):
            raise BadRequest
        update_sites_in_io(data.get('url'), updated_url=data.get('new_url'))
        return None, 204

    @staticmethod
    @api.expect(site)
    @api.response(204, 'Site successfully deleted from monitoring.')
    def delete():
        """
        Deletes site from monitoring.
        * Send a JSON object with the URL in request body.
        ```
        {
          "url": "Current URL"
        }
        ```
        Returns list of sites.
        """
        data = request.json
        if not data.get('url'):
            raise BadRequest
        update_sites_in_io(data.get('url'), delete=True)
        return None, 204


@ns_monitoring.route('/')
class Monitoring(Resource):
    """
    Contains endpoint for site monitoring
    """
    @staticmethod
    @api.marshal_list_with(site_status)
    def get():
        """
        Returns list of sites with current status.
        """

        return [v for k, v in test_sites()]
