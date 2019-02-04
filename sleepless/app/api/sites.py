import time
import datetime
import requests
from flask import request
from flask_restplus import Resource, fields
from app.api.restplus import api
from app.api.io_logic import get_sites_from_io, update_sites_in_io
from werkzeug.exceptions import BadRequest


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


@ns_sites.route('/')
class SitesCollection(Resource):

    @api.marshal_list_with(site)
    def get(self):
        """
        Returns list of sites.
        """
        return [v for k, v in get_sites_from_io().items()]

    @api.response(201, 'URL successfully added.')
    @api.expect(site)
    def post(self):
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

    @api.expect(site_update)
    @api.response(204, 'Site successfully updated.')
    def put(self):
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


    @api.expect(site)
    @api.response(204, 'Site successfully deleted from monitoring.')
    def delete(self):
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

    @api.marshal_list_with(site_status)
    def get(self):
        """
        Returns list of sites with current status.
        """
        sites = get_sites_from_io().items()
        for key, site in sites:
            start = time.time()
            try:
                r = requests.get(site.get('url'), timeout=2)
            except requests.exceptions.MissingSchema:
                site['last_status'] = 'No schema supplied'
                continue
            except requests.exceptions.ConnectionError:
                site['last_status'] = 'Connection Error'
                continue
            except Exception:
                site['last_status'] = 'Error'
                continue
            elapsed = time.time() - start
            if r.status_code == requests.codes.ok and elapsed <= 0.25:
                site['last_status'] = 'OK'
            elif r.status_code == requests.codes.ok:
                site['last_status'] = 'Slow'
            else:
                site['last_status'] = 'Error'
            site['last_checked'] = datetime.datetime.fromtimestamp(start)
        return [v for k, v in sites]
