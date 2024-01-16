# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, QueryGNQA
from apps.authentication.models import Users
from apps.authentication.util import verify_pass

from apps.apihandler.process import getGNQA

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            #return redirect(url_for('authentication_blueprint.route_default'))
            return redirect(url_for('authentication_blueprint.gnqa'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    #return redirect(url_for('home_blueprint.index'))
    return render_template('/home/gnqa.html') # redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)
'''
    return render_template('accounts/login.html',
                           msg='Registration is disabled for this site.')
'''

@blueprint.route('/gnqa', methods=['POST', 'GET'])
def gnqa():
    if not current_user.is_authenticated:
        return redirect(url_for('authentication_blueprint.login'))
    else:
        print('Current user {0}'.format(current_user))
        queryForm = QueryGNQA(request.form)
        if request.method == 'GET':
            return render_template('home/gnqa.html')
        if request.method == 'POST':
            query = request.form['querygnqa']
            answer, refs = getGNQA(query)
            return render_template('home/gnqa.html',
                    query=query, answer=answer,
                    accordion_refs=refs, form=queryForm)
        else:
            return render_template('home/gnqa.html')
        
@blueprint.route('gnqatest', methods=['POST', 'GET'])
def gnqatest():
    return render_template('home/gnqatest.html')

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
