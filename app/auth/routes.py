from app import db
from flask_login import login_user, logout_user
from flask import render_template, redirect, flash, url_for, request
from app.auth.forms import LoginForm, RegisterForm
from app.models import User
from app.auth import bp
import sqlalchemy as sa
from urllib.parse import urlsplit


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = request.form['username']
        email = request.form.get('email')
        password = request.form.get('password')

        query = sa.select(User).where(User.email == email)
        user = db.session.scalar(query)

        if not user:
            user = User(
                username=username,
                email=email,
            )
            user.set_password(password)
            print(user)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('blog.blog'))
        else:
            flash("You've already signed up with that email,")
            return redirect(url_for('auth.register'))
    return render_template("auth/register.html", form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        query = sa.select(User).where(User.email == email)
        user = db.session.scalar(query)
        print(user)
        if not user:
            flash('Email does not exist, please try again.')
            return redirect(url_for('auth.login'))
        else:
            is_correct = user.check_password(password)
            if is_correct:
                login_user(user)
                # flash(Markup('<i class="bi bi-check-circle-fill fs-1"></i> Logged in successfully.'), 'success')
                next_page = request.form.get('next-page')
                if not next_page or urlsplit(next_page).netloc != '':
                    next_page = url_for('blog.blog')
                return redirect(next_page)
            else:
                flash('Password incorrect, please try again.')
    return render_template("auth/login.html", form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

