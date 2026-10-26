from flask import Flask, Blueprint, render_template, request, redirect, abort, url_for, make_response
import flask_login
import phonenumbers 
from phonenumbers import NumberParseException, PhoneNumberFormat, region_code_for_number, timezone, geocoder
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
    user.role = user_doc.get("role")
    return user

def validate_phone(phone_number, default_region="US"):
    if not phone_number:            #true if blank
        return True
    try:
        parsed = phonenumbers.parse(phone_number.strip(), default_region)
        format_check = phonenumbers.is_possible_number(parsed)
        region_check = region_code_for_number(parsed) 
        return format_check and region_check is not None

    except NumberParseException:
        return False


def get_phone_meta(phone_number, default_region="US"):
    if not phone_number:
        return None
    try:
        parsed = phonenumbers.parse(phone_number.strip(), default_region)
        if not (phonenumbers.is_possible_number(parsed) and region_code_for_number(parsed)):
            return None
        location_name = geocoder.description_for_number(parsed, "en")
        zones = timezone.time_zones_for_number(parsed)
        tz = zones[0] 
        if location_name and tz:
            return f"{location_name} ({tz})" # formats it in location (timezone)
        return location_name or tz           # if one of them fai only show one
    except NumberParseException:
        return None

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
    phone = request.form['phone']
    password = request.form['password']

    teach_skills = parse_skills(request.form.getlist("teach"))
    learn_skills = parse_skills(request.form.getlist("learn"))

    if db.users.find_one({'email': email}):
        return render_template('register.html', error='Email already registered, please pick another')

    if db.users.find_one({'username': username}):
        return render_template('register.html', error='Username already registered, please pick another')

    # checks that phone isn't "" -> means user didn't register w/ phone #
    if phone and db.users.find_one({'phone': phone}):
        return render_template('register.html', error='This phone number is already registered, please use another')

    if not validate_phone(phone):
        return render_template('register.html', error='Please enter a valid phone number')

    location = get_phone_meta(phone)
    location_verified = bool(location)

    db.users.insert_one({
        'email': email,
        'username' : username,
        'password': generate_password_hash(password),  #hashes password so it isn't plaintext
        'phone': phone,
        'location': location,
        "location_verified": location_verified,
        'teach_skills': teach_skills,
        'learn_skills': learn_skills,
        'role': 'member'
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