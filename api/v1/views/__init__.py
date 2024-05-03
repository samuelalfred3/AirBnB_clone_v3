#!/usr/bin/python3
"""Initialization module for views of v1 of the API."""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of all view modules
from api.v1.views.index import *

