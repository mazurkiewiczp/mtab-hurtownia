#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import MySQLdb as MS
from subprocess import Popen, PIPE

class SQLClient(object):
    """Klient do obsługi bazy danych"""
    def __init__(self):
        self.data_base = MS.connetct(host='localhost', user='root', passwd='1234')
        self._init_database()

    def get_table_data(self, table_name):
        """Pobieranie danych z wskazanej tabeli"""
        return "Dane z tabeli: " + table_name

    def _init_database():
        """Tworzy bazę danych jeżeli nie istnieje"""
        user = "root"
        passwd = "1234"
        db = "mtab_db"
        filename = mtab.sql
        process = Popen(['mysql', db, '-u', user, '-p', passwd],
                                stdout=PIPE, stdin=PIPE)
        output = process.communicate('source ' + filename)[0]
