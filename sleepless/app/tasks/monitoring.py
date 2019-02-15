import os
from app.api.sites import test_sites
from app import create_celery_app
from flask_socketio import SocketIO


celery = create_celery_app()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, test_domains, name='Every 30s check domains')


@celery.task
def test_domains():
    socket_io = SocketIO(message_queue=os.environ.get('CELERY_BROKER'))
    socket_io.emit('sites_event', {'results': [v for k, v in test_sites()]}, broadcast=True)

