from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# tuzafata db tuyihabwe na app.py nyuma
db = None

def init_db(database):
    global db
    db = database


@auth_bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed = generate_password_hash(request.form['password'])

        user = {
            'name': request.form['name'],
            'email': request.form['email'],
            'regNo': request.form['regNo'],
            'class': request.form['class'],
            'password': hashed,
            'role': 'student'
        }

        db.users.insert_one(user)
        return redirect('/login')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        regNo = request.form['regNo']
        password = request.form['password']

        user = db.users.find_one({'regNo': regNo})

        if user and check_password_hash(user['password'], password):
            session['name'] = user['name']
            session['role'] = user['role']
            session['class'] = user['class']

            if session['role'] == 'student':
                return redirect('/student')
            else:
                return redirect('/teacher')
           

        flash("Invalid Credentials")

    return render_template('login.html')
