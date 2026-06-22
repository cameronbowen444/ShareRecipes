from flask_app import app 
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_app.models import recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def index2():
    return render_template('/index2.html')


@app.route('/validate-register', methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/register')
    
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    
    user_id = user.User.save(data)
    session['user_id'] = user_id

    return redirect('/dashboard')

@app.route('/validate-login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Email and password are required.', 'login')
        return redirect('/')

    users = user.User.get_email({"email": email})

    if not users:
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(users.password, password):
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    session['user_id'] = users.id

    return redirect('/dashboard')


@app.route('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    logged_user = user.User.get_id(data)

    return render_template(
        'dashboard.html',
        user=logged_user,
        recipe=recipe.Recipe.get_recipes()
    )


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')