
from flask_app import app  
from flask_app.models import user
from flask_app.models.user import User
from flask import render_template, request, session, flash, redirect
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login():
    return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

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
    id = user.User.add_user(data)
    session['id'] = id
    return redirect('/dashboard')

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
    session['id'] = user_from_db.id
    return redirect('/dashboard')

# @app.route('/user/<int:id>')
# def user_page(id):
#     if 'id' in session:
#         if session['id'] == id:
#             data = {
#                 "id" : id
#             }
#             return render_template('user_page.html', user = user.User.grab_one(data))
#         else:
#             flash('You are not authorized to view that page.', 'error')
#             return redirect('/')
#     else:
#         flash('You must be logged in to view that page', 'error')
#         return redirect('/')


# user edit - display route
@app.route("/user/<int:id>")
def edit_user(id):
    user_data = {
        'id': session['id']
    }
    session_user = User.get_user_by_id(user_data)
    return render_template("edit_profile.html", session_user=session_user)


# user edit - process route
@app.route("/user/<int:id>/update", methods=["POST"])
def update_user(id):
    if not user.User.validate_user_update(request.form):
        return redirect(f"/user/{id}")
    user.User.update(request.form)
    return redirect("/dashboard")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')