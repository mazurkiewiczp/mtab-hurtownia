#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import crypt
from flask import Flask, session, redirect, url_for, request, render_template
from flask_restful import Resource, Api
from mysql_client import SQLClient
from OpenSSL import SSL
import cmd.users as users

# from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
base = SQLClient()
base.get_table_data('Pracownik')


context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')

#class Pracownik(Resource):
#    def delete(self, id):
#        return base.delete_pracownik(id)
#    def get(self, id):
#        return self.delete(id)


def _check_password(login, password):
    """sprawdzanie hasła"""
    keys = users.get_users()
    if login in keys.keys() and crypt.crypt(password, 'pw') == keys[login]:
        return True
    return False


@app.route('/index.html', methods=['GET', 'POST'])
@app.route('/')
def index():
    if 'login' in session:
        return render_template('index.html', user=session['login'])
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if _check_password(request.form['login'], request.form['password']):
            session['login'] = request.form['login']
            return redirect(url_for('index'))
    return render_template('login.html', info='Incorrect')


@app.route('/logout')
def logout():
    """Wylogowanie uzytkownika"""
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
                           firma=base.get_table_data('Firma'),
                           zamowienia_produkty=base.get_zamowienia_produkty()
                           )


@app.route('/magazyn', methods=['GET', 'POST'])
@app.route('/magazyn.html', methods=['GET', 'POST'])
def magazyn():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['id_produktu'] and request.form['ilosc']:
            print(base.add_magazyn(
                request.form['id_produktu'],
                request.form['ilosc'],
                request.form['komentarz'],
            ))
    return render_template('magazyn.html',
                           magazyn=base.get_table_data('Magazyn'),
                           produkt=base.get_table_data('Produkt'),
                           kategoria=base.get_table_data('Kategoria'),
                           firma=base.get_table_data('Firma'),
                           zamowienia_produkty=base.get_zamowienia_produkty()
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
        wszystko=base.get_pracownicy(),
        pracownik=base.get_table_data("Pracownik"),
        etat=base.get_table_data("Etat"),
        stanowisko=base.get_table_data("Stanowisko")
    )

@app.route('/katalog', methods=['GET', 'POST'])
@app.route('/katalog.html', methods=['GET', 'POST'])
def katalog():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['id_kategorii'] and request.form['nazwa'] and request.form['opis'] and request.form['cena_sugerowana']:
            print(base.add_produkt(
                request.form['id_kategorii'],
                request.form['id_firmy'],
                request.form['nazwa'],
                request.form['opis'],
                request.form['cena_sugerowana']
            ))
    return render_template(
        'katalog.html',
        firma=base.get_table_data("Firma"),
        kategoria=base.get_table_data("Kategoria"),
        produkt=base.get_table_data("Produkt")
    )

@app.route('/nowy_etat', methods=['GET', 'POST'])
def nowy_etat():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['od'] and request.form['id_stanowiska'] and request.form['id_pracownika']:
            print(base.add_etat(
                request.form['od'],
                request.form['pensja'],
                request.form['id_stanowiska'],
                request.form['id_pracownika'],
                request.form['do'],
            ))
    return render_template(
        'pracownicy.html',
        wszystko=base.get_pracownicy(),
        pracownik=base.get_table_data("Pracownik"),
        etat=base.get_table_data("Etat"),
        stanowisko=base.get_table_data("Stanowisko")
    )

@app.route('/nowa_firma', methods=['GET', 'POST'])
def nowa_firma():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['rodzaj_firmy'] and request.form['nazwa_firmy']:
            print(base.add_firma(
                request.form['rodzaj_firmy'],
                request.form['nazwa_firmy'],
                request.form['adres'],
                request.form['telefon']
            ))
    return render_template(
        'katalog.html',
        firma=base.get_table_data("Firma"),
        kategoria=base.get_table_data("Kategoria"),
        produkt=base.get_table_data("Produkt")
    )


@app.route('/nowe_stanowisko', methods=['GET', 'POST'])
def nowe_stanowisko():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['stanowisko']:
            print(base.add_stanowisko(
                request.form['stanowisko']
            ))
    return render_template(
        'pracownicy.html',
        wszystko=base.get_pracownicy(),
        pracownik=base.get_table_data("Pracownik"),
        etat=base.get_table_data("Etat"),
        stanowisko=base.get_table_data("Stanowisko")
    )

@app.route('/nowa_kategoria', methods=['GET', 'POST'])
def nowa_kategoria():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['kategoria']:
            print(base.add_kategoria(
                request.form['kategoria']
            ))
    return render_template(
        'katalog.html',
        firma=base.get_table_data("Firma"),
        kategoria=base.get_table_data("Kategoria"),
        produkt=base.get_table_data("Produkt")
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
                           firma=base.get_table_data('Firma'),
                           zamowienia_produkty=base.get_zamowienia_produkty()                           
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
                           kategoria=base.get_table_data('Kategoria'),
                           zamowienia_lista=base.get_zamowienia_lista(),
                           zamowienia_produkty=base.get_zamowienia_produkty()			
                           )

@app.route('/zamowienia_t', methods=['GET', 'POST'])
def zamowienia_t():
    if not "login" in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['id_firmy'] and request.form['data'] and request.form['rodzaj_transakcji'] and request.form['id_zamowienia']:
            print(base.add_transakcja_hurtowa(
                request.form['id_firmy'],
                request.form['data'],
                request.form['rodzaj_transakcji'],
                request.form['id_zamowienia']
            ))
    return render_template('zamowienia.html',
                           transakcja_hurtowa=base.get_table_data('Transakcja_hurtowa'),
                           zamowienie=base.get_table_data("Zamowienie"),
                           produkt=base.get_table_data('Produkt'),
                           firma=base.get_table_data('Firma'),
                           kategoria=base.get_table_data('Kategoria'),
                           zamowienia_lista=base.get_zamowienia_lista(),
                           zamowienia_produkty=base.get_zamowienia_produkty()			
                           )

@app.route('/stanowisko/<int:stanowisko_id>')
def usun_stanowisko(stanowisko_id):
    if not "login" in session:
        return redirect(url_for('login'))
    print(base.delete_stanowisko(stanowisko_id))
    return render_template(
        'pracownicy.html',
        wszystko=base.get_pracownicy(),
        pracownik=base.get_table_data("Pracownik"),
        etat=base.get_table_data("Etat"),
        stanowisko=base.get_table_data("Stanowisko")
    )

@app.route('/pracownik/<int:id_pracownika>')
def usun_pracownika(id_pracownika):
    if not "login" in session:
        return redirect(url_for('login'))
    print(base.delete_pracownik(id_pracownika))
    return render_template(
        'pracownicy.html',
        wszystko=base.get_pracownicy(),
        pracownik=base.get_table_data("Pracownik"),
        etat=base.get_table_data("Etat"),
        stanowisko=base.get_table_data("Stanowisko")
    )


@app.route('/magazyn/<int:id_towaru>')
def usun_towar_m(id_towaru):
    if not "login" in session:
        return redirect(url_for('login'))
    print(base.delete_magazyn(id_towaru))
    return render_template('magazyn.html',
                           magazyn=base.get_table_data('Magazyn'),
                           produkt=base.get_table_data('Produkt'),
                           kategoria=base.get_table_data('Kategoria'),
                           firma=base.get_table_data('Firma'),
                           zamowienia_produkty=base.get_zamowienia_produkty()
                           )

@app.route('/sklep/<int:id_towaru>')
def usun_towar_s(id_towaru):
    if not "login" in session:
        return redirect(url_for('login'))
    print(base.delete_sklep(id_towaru))
    return render_template('sklep.html',
                           sklep_detaliczny=base.get_table_data("Sklep_detaliczny"),
                           produkt=base.get_table_data('Produkt'),
                           kategoria=base.get_table_data('Kategoria'),
                           firma=base.get_table_data('Firma'),
                           zamowienia_produkty=base.get_zamowienia_produkty()                           
                           )

@app.route('/kategoria/<int:id_kategorii>')
def usun_kategorie(id_kategorii):
    if not "login" in session:
        return redirect(url_for('login'))
    print(base.delete_kategoria(id_kategorii))
    return render_template(
        'katalog.html',
        firma=base.get_table_data("Firma"),
        kategoria=base.get_table_data("Kategoria"),
        produkt=base.get_table_data("Produkt")
    )

@app.route('/firma/<int:id_firmy>')
def usun_firme(id_firmy):
    if not "login" in session:
        return redirect(url_for('login'))
    print(base.delete_firma(id_firmy))
    return render_template(
        'katalog.html',
        firma=base.get_table_data("Firma"),
        kategoria=base.get_table_data("Kategoria"),
        produkt=base.get_table_data("Produkt")
    )

@app.route('/produkt/<int:id_produkt>')
def usun_produkt(id_produkt):
    if not "login" in session:
        return redirect(url_for('login'))
    print(base.delete_produkt(id_produkt))
    return render_template(
        'katalog.html',
        firma=base.get_table_data("Firma"),
        kategoria=base.get_table_data("Kategoria"),
        produkt=base.get_table_data("Produkt")
    )

app.secret_key = 'Ba2ArN13w01N1k0W'
context = ('server.crt', 'server.key')
#api.add_resource(Pracownik, '/pracownik/<int:id>')
app.run(ssl_context=context)
