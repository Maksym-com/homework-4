from flask import Blueprint

bp = Blueprint('/', __name__)

from app.main import routes
