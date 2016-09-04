#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from flask import Flask, session, redirect, url_for, request, render_template
from mysql_client import SQLClient

# from flask_restful import Resource, Api

app = Flask(__name__)
base = SQLClient()
base.get_table_data('Pracownik')

def _check_password(login, password):
    """sprawdzanie hasła"""
    keys = {'ja': "1234", "admin": "admin"}
    if login in keys.keys() and password == keys[login]:
        return True
    return False

@app.route('/')
def index():
    if 'login' in session:
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/index.html', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if _check_password(request.form['login'], request.form['password']):
            session['login'] = request.form['login']
            return redirect(url_for('index'))
    return render_template('login.html', info='Incorrect')


@app.route('/logout')
def logout():
    """Wylogowanie urzytkownika"""
    session.pop('login', None)
    return redirect(url_for('index'))


@app.route('/det', methods=['GET', 'POST'])
@app.route('/det.html', methods=['GET', 'POST'])
def det():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['id_produktu'] and request.form['cena'] and request.form['ilosc'] and request.form['data']:
            print(base.add_transakcje_detaliczne(
                request.form['id_produktu'],
                request.form['cena'],
                request.form['ilosc'],
                request.form['data']
            ))
    return render_template('det.html',
                           transakcje_detaliczne=base.get_table_data('Transakcje_detaliczne'),
                           produkt=base.get_table_data('Produkt'),
                           kategoria=base.get_table_data('Kategoria'),
                           firma=base.get_table_data('Firma')
                           )


@app.route('/magazyn', methods=['GET', 'POST'])
@app.route('/magazyn.html', methods=['GET', 'POST'])
def magazyn():
    if not "login" in session:
        return redirect(url_for('login'))
    return render_template('magazyn.html',
                           magazyn=base.get_table_data('Magazyn'),
                           produkt=base.get_table_data('Produkt'),
                           kategoria=base.get_table_data('Kategoria'),
                           firma=base.get_table_data('Firma')
                           )


@app.route('/pracownicy', methods=['GET', 'POST'])
@app.route('/pracownicy.html', methods=['GET', 'POST'])
def pracownicy():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['imie'] and request.form['nazwisko']:
            print(base.add_employee(
                request.form['imie'],
                request.form['nazwisko'],
                request.form['telefon'],
                request.form['mail']
            ))
    return render_template(
        'pracownicy.html',
        pracownik=base.get_table_data("Pracownik"),
        etat=base.get_table_data("Etat"),
        stanowisko=base.get_table_data("Stanowisko")
    )


@app.route('/sklep', methods=['GET', 'POST'])
@app.route('/sklep.html', methods=['GET', 'POST'])
def sklep():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['id_produktu'] and request.form['cena_produktu']:
            print(base.add_sklep_detaliczny(
                request.form['id_produktu'],
                request.form['cena_produktu'],
                request.form['ilosc_na_stanie'],
                request.form['komentarz']
            ))
    return render_template('sklep.html',
                           sklep_detaliczny=base.get_table_data("Sklep_detaliczny"),
                           produkt=base.get_table_data('Produkt'),
                           kategoria=base.get_table_data('Kategoria'),
                           firma=base.get_table_data('Firma')
                           )


@app.route('/zamowienia', methods=['GET', 'POST'])
@app.route('/zamowienia.html', methods=['GET', 'POST'])
def zamowienia():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['id_produktu'] and request.form['cena_produktu'] and request.form['ilosc_produktu']:
            print(base.add_zamowienie(
                request.form['id_produktu'],
                request.form['cena_produktu'],
                request.form['ilosc_produktu'],
            ))
    return render_template('zamowienia.html',
                           transakcja_hurtowa=base.get_table_data('Transakcja_hurtowa'),
                           zamowienie=base.get_table_data("Zamowienie"),
                           produkt=base.get_table_data('Produkt'),
                           firma=base.get_table_data('Firma'),
                           kategoria=base.get_table_data('Kategoria')
                           )


# Wzorzec XXX
@app.route('/stanowisko', methods=['GET', 'POST'])
def stanowisko():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['opis_stanowiska']:
            print(base.add_stanowisko(
                request.form['opis_stanowiska']
            ))
    return base.get_table_data('Stanowisko')


app.secret_key = 'Ba2ArN13w01N1k0W'

app.run()
