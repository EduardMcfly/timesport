from flask import render_template, request, jsonify
from flask.blueprints import Blueprint

from database import getSession
from models.User import User

signUpBp = Blueprint(
    'signUp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/signUp'
)


@signUpBp.route("/signUp", methods=['GET', 'POST'])
def index():
    method = request.method
    if(method == 'POST'):
        name = request.form.get('name')
        password = request.form.get('password')

        session = getSession()
        try:
            user = User()
            user.name = name
            user.password = password
            session.add(user)

            # This is to save the data
            session.commit()
            return "Data saved"
        except Exception as error:
            session.rollback()
            raise error
    return render_template('signUp.html')
