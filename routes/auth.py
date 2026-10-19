import flask
import flask_login
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash  #flask secruity thing
from db import db
from flask import session

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
        return flask.render_template('login.html', signing_up=False)

    email = flask.request.form['email']
    password = flask.request.form['password']

    user_doc = db.users.find_one({'email': email}) # look up user by email
    if user_doc and check_password_hash(user_doc['password'], password):
        user = User()                       #creates session and makes user id from mongoid
        user.id = str(user_doc['_id'])
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('profile.my_profile'))  #user profile page

    return flask.render_template('login.html', error="Invalid email or password.")

def parse_skills(raw):
    names = [s.strip().title() for s in raw.split(',') if s.strip()]
    return [{'name': name, 'proficiency': '', 'description': '', 'images': []} for name in names]

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'GET':
       return flask.render_template('register.html', signing_up=True)
    
    username = flask.request.form['username']
    email = flask.request.form['email']
    password = flask.request.form['password']

    teach_skills = parse_skills(flask.request.form.get('teach_skills', ''))
    learn_skills = parse_skills(flask.request.form.get('learn_skills', ''))

    if db.users.find_one({'email': email}):
        return 'Email already registered, please pick another'

    db.users.insert_one({
        'email': email,
        'username' : username,
        'password': generate_password_hash(password),  #hashes password so it isn't plaintext
        'teach_skills': teach_skills,
        'learn_skills': learn_skills,
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