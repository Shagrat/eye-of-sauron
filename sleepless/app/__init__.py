from flask import Flask, Blueprint
from app.api.restplus import api
from app.api.sites import ns_sites, ns_monitoring
from app.views.dashboard import ShowDashboard


def create_app():
    app = Flask(__name__)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(ns_sites)
    api.add_namespace(ns_monitoring)
    app.register_blueprint(blueprint)
    app.add_url_rule('/', view_func=ShowDashboard.as_view('show_dashboard'))
    return app
