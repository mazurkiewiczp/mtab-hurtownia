#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import MySQLdb as MS
from subprocess import Popen, PIPE

DB_NAME = 'mtab_db'
LOG_FILE_NAME = '~/.base_errors.log'

def log(e):
    with open(LOG_FILE_NAME, "a") as logfile:
        logfile.write(e)

class SQLClient(object):
    """Klient do obsługi bazy danych"""
    def __init__(self):
        try:
            self.data_base = MS.connect(host='localhost', user='root', passwd='1234')
            self._init_database()
            self.data_base.autocommit(True)
        except Exception as e:
            log(e)

    def get_pracownicy(self):
        """Pobieranie wszystkiego z tabel Pracownik, Etat, Stanowisko"""
        sql = """select Pracownik.*, Etat.id_etatu, Etat.od, Etat.do, Etat.pensja, Stanowisko.id_stanowiska, Stanowisko.opis_stanowiska from Pracownik left join Etat on Etat.id_pracownika = Pracownik.id_pracownika left join Stanowisko on Etat.id_stanowiska = Stanowisko.id_stanowiska;
"""
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def get_zamowienia_lista(self):
        sql = """select Zamowienie.*, Transakcja_hurtowa.id_transakcji, Transakcja_hurtowa.id_firmy, Transakcja_hurtowa.data, Transakcja_hurtowa.rodzaj_transakcji from Zamowienie left join Transakcja_hurtowa on Zamowienie.id_zamowienia = Transakcja_hurtowa.id_zamowienia;"""
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def get_zamowienia_produkty(self):
        sql = """select Produkt.id_produktu, Produkt.id_kategorii, Kategoria.opis_kategorii, Produkt.id_firmy, Firma.nazwa_firmy, Firma.rodzaj_firmy, Firma.adres, Firma.telefon, Produkt.nazwa, Produkt.opis, Produkt.cena_sugerowana from Produkt left join Kategoria on Produkt.id_kategorii = Kategoria.id_kategorii left join Firma on Produkt.id_firmy = Firma.id_firmy;"""
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def get_table_data(self, table_name):
        """Pobieranie danych z wskazanej tabeli"""
        sql = """SELECT * FROM %s;"""
        try:
            self.cursor.execute(sql % (table_name,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_employee(self, imie, nazwisko, telefon=None, mail=None):
        """Dodaje pracownika"""
        sql = """INSERT INTO Pracownik (imie, nazwisko, telefon, mail) VALUES (%s, %s, %s, %s);"""
        try:
            self.cursor.execute(sql, (imie, nazwisko, telefon, mail))
            result = self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e
        return result

    def add_etat(self, od, pensja, id_stanowiska, id_pracownika, do=None):
        """Dodaje etat"""
        sql = """INSERT INTO Etat (od, do, pensja, id_stanowiska, id_pracownika) VALUES (%s, %s, %s, %s, %s);"""
        try:
            self.cursor.execute(sql, (od, do, pensja, id_stanowiska, id_pracownika))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_stanowisko(self, opis_stanowiska):
        """Dodaje stanowisko"""
        sql = """INSERT INTO Stanowisko (opis_stanowiska) VALUES (%s);"""
        try:
            self.cursor.execute(sql, (opis_stanowiska,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_kategoria(self, opis_kategorii):
        """Dodaje kategorie"""
        sql = """INSERT INTO Kategoria (opis_kategorii) VALUES (%s);"""
        try:
            self.cursor.execute(sql, (opis_kategorii,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_firma(self, rodzaj_firmy, nazwa_firmy, adres=None, telefon=None):
        """Dodaje firme"""
        sql = """INSERT INTO Firma (rodzaj_firmy, nazwa_firmy, adres, telefon) VALUES (%s, %s, %s, %s);"""
        try:
            self.cursor.execute(sql, (rodzaj_firmy, nazwa_firmy, adres, telefon))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_produkt(self, id_kategorii, id_firmy, nazwa, opis, cena_sugerowana):
        """Dodaje produkt"""
        sql = """INSERT INTO Produkt (id_kategorii, id_firmy, nazwa, opis, cena_sugerowana) VALUES (%s, %s, %s, %s, %s);"""
        try:
            self.cursor.execute(sql, (id_kategorii, id_firmy, nazwa, opis, cena_sugerowana))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_magazyn(self, id_produktu, ilosc, komentarz=None):
        """Dodaje magazyn"""
        sql = """INSERT INTO Magazyn (id_produktu, ilosc, komentarz) VALUES (%s, %s, %s);"""
        try:
            self.cursor.execute(sql, (id_produktu, ilosc, komentarz))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_sklep_detaliczny(self, id_produktu, cena_produktu, ilosc_na_stanie=None, komentarz=None):
        """Dodaje sklep detaliczny"""
        sql = """INSERT INTO Sklep_detaliczny (id_produktu, cena_produktu, ilosc_na_stanie, komentarz) VALUES (%s, %s, %s, %s);"""
        try:
            self.cursor.execute(sql, (id_produktu, cena_produktu, ilosc_na_stanie, komentarz))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_transakcje_detaliczne(self, id_produktu, cena, ilosc, data):
        """Dodaje transakcje detaliczna"""
        sql = """INSERT INTO Transakcje_detaliczne (id_produktu, cena, ilosc, data) VALUES (%s, %s, %s, %s);"""
        try:
            self.cursor.execute(sql, (id_produktu, cena, ilosc, data))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_zamowienie(self, id_produktu, cena_produktu, ilosc_produktu):
        """Dodaje zamowienie"""
        sql = """INSERT INTO Zamowienie (id_produktu, cena_produktu, ilosc_produktu) VALUES (%s, %s, %s);"""
        try:
            self.cursor.execute(sql, (id_produktu, cena_produktu, ilosc_produktu))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def add_transakcja_hurtowa(self, id_firmy, data, rodzaj_transakcji, id_zamowienia):
        """Dodaje pracownika"""
        sql = """INSERT INTO Transakcja_hurtowa (id_firmy, data, rodzaj_transakcji, id_zamowienia) VALUES (%s, %s, %s, %s);"""
        try:
            self.cursor.execute(sql, (id_firmy, data, rodzaj_transakcji, id_zamowienia))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def delete_pracownik(self, id):
        """Usuwa praconika o wskazanym id"""
        sql = """DELETE FROM Etat WHERE id_pracownika = %s"""
        self.cursor.execute(sql, (id,))
        self.cursor.fetchall()
        sql = """DELETE FROM Pracownik WHERE id_pracownika = %s"""
        try:
            self.cursor.execute(sql, (id,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def delete_stanowisko(self, id):
        """Usuwa stanowisko o wskazanym id"""
        sql = """DELETE FROM Stanowisko WHERE id_stanowiska = %s"""
        try:
            self.cursor.execute(sql, (id,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def delete_magazyn(self, id):
        """Usuwa stanowisko o wskazanym id"""
        sql = """DELETE FROM Magazyn WHERE id_towaru = %s"""
        try:
            self.cursor.execute(sql, (id,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def delete_sklep(self, id):
        """Usuwa stanowisko o wskazanym id"""
        sql = """DELETE FROM Sklep_detaliczny WHERE id_towaru = %s"""
        try:
            self.cursor.execute(sql, (id,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def delete_produkt(self, id):
        """Usuwa produkt o wskazanym id"""
        sql = """DELETE FROM Produkt WHERE id_produktu = %s"""
        try:
            self.cursor.execute(sql, (id,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def delete_firma(self, id):
        """Usuwa firme o wskazanym id"""
        sql = """DELETE FROM Firma WHERE id_firmy = %s"""
        try:
            self.cursor.execute(sql, (id,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def delete_kategoria(self, id):
        """Usuwa kategorie o wskazanym id"""
        sql = """DELETE FROM Kategoria WHERE id_kategorii = %s"""
        try:
            self.cursor.execute(sql, (id,))
            return self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e

    def _init_database(self):
        """Tworzy bazę danych jeżeli nie istnieje"""
        try:
            self.cursor = self.data_base.cursor()
            sql = 'USE {};'.format(DB_NAME)
            self.cursor.execute(sql)
            self.cursor.fetchall()
        except Exception as e:
            log(e)
            return e
