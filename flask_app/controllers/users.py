
from flask_app import app  
from flask_app.models import user
from flask import render_template, request, session, flash, redirect
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/user/process', methods=['POST'])
def register_user():
    if not request.form['password']:
        flash('Password field cannot be empty', 'register')
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    if not user.User.validate_user(request.form, data):
        return redirect('/')
    uid = user.User.add_user(data)
    session['uid'] = uid
    return redirect(f'/user/{uid}')

@app.route('/login_check', methods=['POST'])
def login_check():
    if not user.User.validate_login(request.form):
        return redirect('/')
    data = {
        "email": request.form['email']
    }
    user_from_db = user.User.grab_by_email(data)
    if not user_from_db:
        flash('This email is not registered.', 'login')
        return redirect ('/')
    if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        flash('Incorrect password.', 'login')
        return redirect ('/')
    session['uid'] = user_from_db.id
    return redirect(f'/user/{user_from_db.id}')

@app.route('/user/<int:id>')
def user_page(id):
    if 'uid' in session:
        if session['uid'] == id:
            data = {
                "id" : id
            }
            return render_template('user_page.html', user = user.User.grab_one(data))
        else:
            flash('You are not authorized to view that page.', 'error')
            return redirect('/')
    else:
        flash('You must be logged in to view that page', 'error')
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')