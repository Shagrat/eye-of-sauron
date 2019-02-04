from flask import Flask, Blueprint
from app.api.restplus import api
from app.api.sites import ns_sites, ns_monitoring


def create_app():
    app = Flask(__name__)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(ns_sites)
    api.add_namespace(ns_monitoring)
    app.register_blueprint(blueprint)
    return app
