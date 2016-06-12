#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from flask import Flask, session, redirect, url_for, request, render_template
# from flask_restful import Resource, Api

app = Flask(__name__)


@app.route('/')
def index():
    if 'login' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/index.html', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # if password
        session['login'] = request.form['login']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Wylogowanie urzytkownika"""
    session.pop('login', None)
    return redirect(url_for('index'))

app.secret_key = 'Ba2ArN13w01N1k0W'

app.run()
