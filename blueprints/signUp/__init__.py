from flask import render_template, request
from flask.blueprints import Blueprint
from database import getSession

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
        connection = session.connection()
        try:

            connection.execute(
                "INSERT INTO users(name, password) VALUES(%s, %s)",
                name, password
            )

            # This is to save the data used in the transactions (INSERT, UPDATE, DELETE).
            session.commit()
            return "Data saved"
        except Exception as error:
            session.rollback()
            raise error
    return render_template('signUp.html')
