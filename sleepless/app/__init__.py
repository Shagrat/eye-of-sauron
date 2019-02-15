import os

from celery import Celery
from flask import Flask, Blueprint
from app.api.restplus import api
from app.api.sites import ns_sites, ns_monitoring
from app.views.dashboard import ShowDashboard
from flask_socketio import SocketIO, emit


CELERY_BROKER = os.environ.get('CELERY_BROKER')
DATA_PATH = os.environ.get('DATA_PATH')


def create_app():
    """
    Initializes app
    :return: app: Flask app
    """
    app = Flask(__name__)
    app.config.update(
        DATA_PATH=DATA_PATH
    )
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(ns_sites)
    api.add_namespace(ns_monitoring)
    app.register_blueprint(blueprint)
    app.add_url_rule('/', view_func=ShowDashboard.as_view('show_dashboard'))

    socketio = SocketIO(app, message_queue=CELERY_BROKER)

    @socketio.on('connection', namespace='/test')
    def confirmation_message(message):
        emit('confirmation', {'connection_confirmation': message['Connected']})

    return app


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.
    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=CELERY_BROKER)
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
