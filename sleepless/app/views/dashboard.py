"""
Dashboard module provides classes and functions to generate and return HTML
pages as responses
"""
from flask import render_template
from flask.views import View


class ShowDashboard(View):
    """
    Default Index View
    """
    def dispatch_request(self):
        return render_template('index.html')
