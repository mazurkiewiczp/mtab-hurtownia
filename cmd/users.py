#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Skrypt dodający nowych użytkowników"""

from __future__ import absolute_import, print_function

import argparse
import json
import os

import crypt

USERS_FILE = os.getenv("USER_FILE", """../users.json""")

def get_users():
    """Wyświetla użytkowników zdefiniowanych w pliku"""
    try:
        with open(USERS_FILE) as users_file:
            return json.load(users_file)
    except (IOError, ValueError) as e:
        print (e)
    return {}


def _add_user(user, password):
    """Dodaje użytkownika"""
    users = get_users()
    users[user] = crypt.crypt("password", 'pw')
    with open(USERS_FILE, "w") as users_file:
        json.dump(users, users_file)


def _del_user(user):
    users = get_users()
    try:
        del users[user]
        with open(USERS_FILE, "w") as users_file:
            json.dump(users, users_file)
    except KeyError as e:
        print ("Bad user:", e)


def main():
    """Main"""
    parser = argparse.ArgumentParser(
        description='Sktypt odopowiedzialny za zarządzanie użytkownikami mającymi dostęp do panelu')
    parser.add_argument("--user", type=unicode, help='Dodanie użytkownika')
    parser.add_argument("--password", type=unicode, help='Hasło użytkownika')
    parser.add_argument("--list", action='store_true', help='Wyświetla listę użytkowników')
    parser.add_argument("--del_user", type=unicode, help='Usunięcie użytkownika')

    args = parser.parse_args()

    if args.user:
        if not args.password:
            print('Nie podano hasła')
        else:
            _add_user(args.user, args.password)

    if args.del_user:
        _del_user(args.del_user)

    if args.list:
        for user in get_users():
            print(user)


if __name__ == """__main__""":
    main()
