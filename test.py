#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Testy jednostkowo-integracyjne"""

from __future__ import absolute_import, print_function
import unittest

class TestStringMethods(unittest.TestCase):

    def _create_test_pracownik(self):
        pass

    def _delete_test_pracownik(self):
        pass

    def test_create_delete_pracownik(self):
        self._create_test_pracownik()
        self._delete_test_pracownik()

if __name__ == "__main__":
    unittest.main()
