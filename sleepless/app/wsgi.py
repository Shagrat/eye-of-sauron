"""
WSGI module, returns app and provides Flask dev server
"""

from . import create_app

app = create_app()


if __name__ == "__main__":
    app.run()
