import flask
import flask_login
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash  #flask secruity thing
from db import db


auth_bp = flask.Blueprint('auth', __name__)

login_manager = flask_login.LoginManager()

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    user_doc = db.users.find_one({'_id': ObjectId(user_id)})
    if not user_doc:
        return None
    user = User()
    user.id = str(user_doc['_id'])
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user_doc = db.users.find_one({'email': email}) if email else None
    if not user_doc:
        return None
    user = User()
    user.id = str(user_doc['_id'])
    return user



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')

    email = flask.request.form['email']
    password = flask.request.form['password']

    user_doc = db.users.find_one({'email': email}) # look up user by email
    if user_doc and check_password_hash(user_doc['password'], password):
        user = User()                       #creates session and makes user id from mongoid
        user.id = str(user_doc['_id'])
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('auth.protected'))

    return 'Bad login'

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if flask.render.method == 'GET':
       return flask.render_template('login.html')

    email = flask.request.form['email']
    password = flask.request.form['password']

    if db.users.find_one({'email': email}):
        return 'Email already registered, please pick another'

    db.users.insert_one({
        'email': email,
        'password': generate_password_hash(password)  #hashes password so it isn't plaintext
    })

    return flask.redirect(flask.url_for('auth.login'))  #login page


@auth_bp.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@auth_bp.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401