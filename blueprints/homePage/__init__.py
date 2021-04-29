from flask import Blueprint, render_template, request, redirect
from sqlalchemy.sql import text

from database import db, getSession, migrate
from models import *
from utils import query_to_dict


homePageBp = Blueprint(
    'homePage',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/homepage/static'
)

@homePageBp.route("/")
def index():
    return render_template('mainPage.html')
