#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import MySQLdb as MS

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
        sql = 'CREATE DATABASE IF NOT EXISTS hurtownia'
        self.data_base.execute(sql)

