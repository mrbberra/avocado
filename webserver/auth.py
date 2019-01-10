import os
import threading
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, redirect, url_for, request,\
 session, flash, Blueprint

auth_views = Blueprint('auth_views', __name__,
                        template_folder='templates')

def validate_login(username, password):
    print(password_hash)
    print(password)
    print(generate_password_hash(password))
    if check_password_hash(ADMIN_PASSWORD_HASH, password) and username == 'admin':
        print('login validated')
        return True
    else:
        return False


@auth_views.route('/login', methods=['GET', 'POST'])
def login_view():
    if session.get('logged_in', False):
        return redirect(url_for('main_views.admin_view'))
    if request.method == 'POST':
        if validate_login(request.form['username'],request.form['password']):
            session['logged_in'] = True
            flash('You were successfully logged in')
            return redirect(url_for('main_views.admin_view'))
        else:
            return render_template('login.html',
                error='Invalid Credentials. Please try again.')
    else:
        return render_template('login.html', error=None)

@auth_views.route('/logout', methods=['GET','POST'])
def logout_view():
    if not session.get('logged_in', False):
        flash('You are already logged out')
        return redirect(url_for('auth_views.login_view'))
    if request.method == 'POST':
        session['logged_in'] = False
        flash('You were successfully logged out')
        return redirect(url_for('auth_views.login_view'))
    else:
        return render_template('logout.html', error=None)
