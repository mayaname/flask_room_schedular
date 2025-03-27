"""
Program: Auth
Author: Maya Name
Creation Date: 01/05/2025
Revision Date: 
Description: User authentication routes for Flask application


Revisions:

"""

from flask import Blueprint, flash, render_template, redirect, request,  url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.extensions import db
from app.forms import LoginForm
from app.models import User
from urllib.parse import urlparse, urljoin

auth = Blueprint('auth', __name__)

def is_safe_redirect_url(target):
    # Check if the url is safe for redirects 
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return (
        redirect_url.scheme in ('http', 'https') and
        host_url.netloc == redirect_url.netloc
    )

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    head_title = 'Login'
    page_title = 'Room Scheduler Login'

    # Reroute to index if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))

    if form.validate_on_submit():
        user = db.session.query(User).where(User.username == form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid login. Check your username and password.', 
                    'error')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash(f'{user.firstname} {user.lastname} successfully logged in', 'success')

        # Check the 'next' parameter for safe redirection
        next_page = request.form.get('next') or request.args.get('next') 

        if next_page and is_safe_redirect_url(next_page):
            # Redirect safely
            return redirect(next_page)
        # Fallback to a default page
        return redirect(url_for('pages.dept_resv'))


    return render_template('login.html', 
                               head_title=head_title,
                               page_title=page_title, 
                               form=form)

@auth.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    firstname = current_user.firstname
    lastname = current_user.lastname
    logout_user()
    flash(f'{firstname} {lastname} logged out successfully!', 'success')

    next_page = request.form.get('next') or request.args.get('next') 
    if next_page and is_safe_redirect_url(next_page):
        return redirect(next_page)
    return redirect(url_for('pages.index'))
