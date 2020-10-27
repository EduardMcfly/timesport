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
        Username = request.form.get('username')
        email_address = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('password')
        session = getSession()
        print(session)
        connection = session.connection()
        try:
            connection.execute(
                "INSERT INTO public.users(name, username, email_address, password, confirm_password)VALUES( %s, %s, %s, %s, %s)",
                 name,  Username, email_address, password, confirm_password)
                 # This is to save the data used in the transactions (INSERT, UPDATE, DELETE).
            session.commit()
            return "Data saved"
        except Exception as error:
            session.rollback()
            raise error
    return render_template('signUp.html')

