import pytest
import os
from app import create_app


@pytest.fixture
def app(monkeypatch):
    app = create_app()
    monkeypatch.setenv('DATA_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sites.yml'))
    app.config.update(
        DATA_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sites.yml')
    )
    yield app
    try:
        os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sites.yml'))
    except:
        pass


@pytest.fixture
def client(app):
    return app.test_client()


def test_dashboard(app, client):
    rv = client.get('/')
    assert rv.status == '200 OK'


def test_sites_list(app, client):
    rv = client.get('/api/')
    assert rv.status == '200 OK'


def test_sites_add(app, client):
    rv = client.post('/api/sites/', json={'url': 'https://google.com'})
    assert rv.status == '201 CREATED'


def test_modify_modify(app, client):
    rv = client.put('/api/sites/', json={'url': 'https://google.com', 'new_url': 'https://amazon.com'})
    assert rv.status == '204 NO CONTENT'


def test_modify_delete(app, client):
    rv = client.delete('/api/sites/', json={'url': 'https://amazon.com'})
    assert rv.status == '204 NO CONTENT'

def test_monitor(app, client):
    rv = client.get('/api/monitoring/')
    assert rv.status == '200 OK'
