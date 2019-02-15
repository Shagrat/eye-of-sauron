"""
Celery tasks to monitor and emmit updates
"""
import os
from flask_socketio import SocketIO
from app import create_celery_app
from app.api.sites import test_sites


celery = create_celery_app()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Creates periodic tasks after celery is initialized
    :param sender: Celery app
    """
    sender.add_periodic_task(30.0, test_domains, name='Every 30s check domains')


@celery.task
def test_domains():
    """
    Tests domains and emits messages to all clients trough SocketIO
    """
    socket_io = SocketIO(message_queue=os.environ.get('CELERY_BROKER'))
    socket_io.emit('sites_event', {
        'results': [v for k, v in test_sites()]
    }, broadcast=True)
