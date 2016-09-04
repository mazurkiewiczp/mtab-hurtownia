#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import MySQLdb as MS
from subprocess import Popen, PIPE

DB_NAME = 'mtab_db'

class SQLClient(object):
    """Klient do obsługi bazy danych"""
    def __init__(self):
        self.data_base = MS.connect(host='localhost', user='root', passwd='1234')
        self._init_database()
        sql = """CREATE """

    def get_table_data(self, table_name):
        """Pobieranie danych z wskazanej tabeli"""
        sql = """SELECT * FROM %s;"""
        self.cursor.execute(sql % (table_name,))
        return self.cursor.fetchall()

    def add_employee(self, imie, nazwisko, telefon=None, mail=None):
        """Dodaje pracownika"""
        sql = """INSERT INTO Pracownik (imie, nazwisko, telefon, mail) VALUES (%s, %s, %s, %s);"""
        self.cursor.execute(sql, (imie, nazwisko, telefon, mail))
        return self.cursor.fetchall()

    def add_etat(self, od, pensja, id_stanowiska, id_pracownika, do=None):
        """Dodaje etat"""
        sql = """INSERT INTO Etat (od, do, pensja, id_stanowiska, id_pracownika) VALUES (%s, %s, %s, %s, %s);"""
        self.cursor.execute(sql, (od, do, pensja, id_stanowiska, id_pracownika))
        return self.cursor.fetchall()

    def add_stanowisko(self, opis_stanowiska):
        """Dodaje stanowisko"""
        sql = """INSERT INTO Stanowisko (opis_stanowiska) VALUES (%s);"""
        self.cursor.execute(sql, (opis_stanowiska,))
        return self.cursor.fetchall()

    def add_kategoria(self, opis_kategorii):
        """Dodaje kategorie"""
        sql = """INSERT INTO Kategoria (opis_kategorii) VALUES (%s);"""
        self.cursor.execute(sql, (opis_kategorii))
        return self.cursor.fetchall()

    def add_firma(self, rodzaj_firmy, nazwa_firmy, adres=None, telefon=None):
        """Dodaje firme"""
        sql = """INSERT INTO Firma (rodzaj_firmy, nazwa_firmy, adres, telefon) VALUES (%s, %s, %s, %s);"""
        self.cursor.execute(sql, (rodzaj_firmy, nazwa_firmy, adres, telefon))
        return self.cursor.fetchall()

    def add_produkt(self, id_kategorii, nazwa, cena_sugerowana, id_firmy=None, opis=None):
        """Dodaje produkt"""
        sql = """INSERT INTO Produkt (id_kategorii, id_firmy, nazwa, opis, cena_sugerowana) VALUES (%s, %s, %s, %s, %s);"""
        self.cursor.execute(sql, (id_kategorii, id_firmy, nazwa, opis, cena_sugerowana))
        return self.cursor.fetchall()

    def add_magazyn(self, id_produktu, ilosc, komentarz=None):
        """Dodaje magazyn"""
        sql = """INSERT INTO Magazyn (id_produktu, ilosc, komentarz) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (id_produktu, ilosc, komentarz))
        return self.cursor.fetchall()

    def add_sklep_detaliczny(self, id_produktu, cena_produktu, ilosc_na_stanie=None, komentarz=None):
        """Dodaje sklep detaliczny"""
        sql = """INSERT INTO Sklep_detaliczny (id_produktu, cena_produktu, ilosc_na_stanie, komentarz) VALUES (%s, %s, %s, %s);"""
        self.cursor.execute(sql, (id_produktu, cena_produktu, ilosc_na_stanie, komentarz))
        return self.cursor.fetchall()

    def add_transakcje_detaliczne(self, id_produktu, cena, ilosc, data):
        """Dodaje transakcje detaliczna"""
        sql = """INSERT INTO Transakcje_detaliczne (id_produktu, cena, ilosc, data) VALUES (%s, %s, %s, %s);"""
        self.cursor.execute(sql, (id_produktu, cena, ilosc, data))
        return self.cursor.fetchall()

    def add_zamowienie(self, id_produktu, cena_produktu, ilosc_produktu):
        """Dodaje zamowienie"""
        sql = """INSERT INTO Zamowienie (id_produktu, cena_produktu, ilosc_produktu) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, (id_produktu, cena_produktu, ilosc_produktu))
        return self.cursor.fetchall()

    def add_transakcja_hurtowa(self, id_firmy, id_zamowienia, data=None, rodzaj_transakcji=None):
        """Dodaje pracownika"""
        sql = """INSERT INTO Pracownik (id_firmy, data, rodzaj_transakcji, id_zamowienia) VALUES (%s, %s, %s, %s);"""
        self.cursor.execute(sql, (id_firmy, data, rodzaj_transakcji, id_zamowienia))
        return self.cursor.fetchall()

    def _init_database(self):
        """Tworzy bazę danych jeżeli nie istnieje"""
        pass
        self.cursor = self.data_base.cursor()
        # sql = 'CREATE DATABASE IF NOT EXISTS {};'.format(DB_NAME)
        # self.cursor.execute(sql)
        # print (self.cursor.fetchall())
        sql = 'USE {};'.format(DB_NAME)
        self.cursor.execute(sql)
        print (self.cursor.fetchall())
