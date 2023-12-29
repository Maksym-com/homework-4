from flask import Blueprint

bp = Blueprint('spendings', __name__)

from app.spendings import routes