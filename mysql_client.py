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

    def _init_database(self):
        """Tworzy bazę danych jeżeli nie istnieje"""
        self.cursor = self.data_base.cursor()
        sql = 'CREATE DATABASE IF NOT EXISTS {};'.format(DB_NAME)
        self.cursor.execute(sql)
        print (self.cursor.fetchall())
        sql = 'USE {};'.format(DB_NAME)
        self.cursor.execute(sql)
        print (self.cursor.fetchall())
