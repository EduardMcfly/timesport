from flask import render_template, request, redirect
from flask.blueprints import Blueprint
from flask.helpers import url_for
from flask_login import login_user
from flask_login.utils import login_required, logout_user
import bcrypt
from flask_login import current_user

from database import getSession
from models.User import User

authenticationBp = Blueprint(
    'authentication',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/authentication'
)


@authenticationBp.route("/login")
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('main'))
    return render_template('login.html')


def toBytes(text: str):
    return bytes(text, encoding='utf-8')


@authenticationBp.route("/login", methods=['POST'])
def loginPost():
    email = request.form.get('email')
    password = toBytes(request.form.get('password'))
    session = getSession()
    user = session.query(User).filter_by(email=email).first()
    hashed = toBytes(user.password)
    if bcrypt.checkpw(password, hashed):
        login_user(user)
        if 'url' in request.session:
            return redirect(session['url'])
        return redirect(url_for('main'))
    else:
        return "Constraseña incorrecta"


@authenticationBp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))


@authenticationBp.route("/user")
def user():
    return render_template('user.html')


@authenticationBp.route("/signUp", methods=['GET', 'POST'])
def signUp():
    method = request.method
    if(method == 'POST'):
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = toBytes(request.form.get('password'))
        session = getSession()
        try:
            user = User()
            user.email = email
            user.name = name
            user.lastname = lastname
            hashed = bcrypt.hashpw(
                password, bcrypt.gensalt()
            )
            user.password = hashed.decode("utf-8")
            session.add(user)
            session.commit()
            login_user(user)
            return redirect(url_for('main'))
        except Exception as error:
            session.rollback()
            raise error
    return render_template('signUp.html')
