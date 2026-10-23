from flask import Flask, Blueprint, render_template, request, redirect, abort, url_for, make_response
import flask_login
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash  #flask secruity thing
from db import db
from flask import session

auth_bp = Blueprint('auth', __name__)

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
    username = request.form.get('username')
    user_doc = db.users.find_one(       #query specification 
        {
            '$or': [    
            {'email': email},
            {'username': username} 
            ]
        }
    )


    if not user_doc:
        return None
    user = User()
    user.id = str(user_doc['_id'])
    return user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    userOrEmail = request.form['username']
    password = request.form['password']

    user_doc = db.users.find_one(       #searches for either email or username, valid if either are found
        {
            '$or': [    
            {'email': userOrEmail},
            {'username': userOrEmail} 
            ]
        }
    )

    if user_doc and check_password_hash(user_doc['password'], password):
        user = User()                             #creates session and makes user id from mongoid
        user.id = str(user_doc['_id'])
        flask_login.login_user(user)
        return redirect(url_for('profile.my_profile'))  #user profile page

    return render_template('login.html', error="Invalid username/email or password.")

def parse_skills(raw):
    names = [s.strip().title() for s in raw if s.strip()]
    return [{'name': name, 'proficiency': '', 'description': '', 'images': []} for name in names]

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if flask_login.current_user.is_authenticated:  # fixes issue somehow of counting person as authenticated when they mess up registration
            flask_login.logout_user()

    if request.method == 'GET':
       return render_template('register.html')

    
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    teach_skills = parse_skills(request.form.getlist("teach"))
    learn_skills = parse_skills(request.form.getlist("learn"))

    if db.users.find_one({'email': email}):
        return render_template('register.html', error='Email already registered, please pick another')

    if db.users.find_one({'username': username}):
        return render_template('register.html', error='Username already registered, please pick another')

    db.users.insert_one({
        'email': email,
        'username' : username,
        'password': generate_password_hash(password),  #hashes password so it isn't plaintext
        'teach_skills': teach_skills,
        'learn_skills': learn_skills,
    })

    return redirect(url_for('auth.login'))  #login page

@auth_bp.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@auth_bp.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('auth.login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401