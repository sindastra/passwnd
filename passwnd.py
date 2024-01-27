#!/usr/bin/env python3
#
# passwnd - Check for breached passwords with k-anonymity
# Copyright (C) 2022  Sindastra <https://github.com/sindastra/passwnd>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License (version 3) for more details.
#
# You should have received a copy of the GNU General Public License (version 3)
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import getpass
import sys
from sys import exit  # This is for pyinstaller to work
from hashlib import sha1
import urllib.request
import os
import platform

APP_VERSION = 'DEV'
PYTHON_VERSION = platform.python_version()

print(F'''passwnd (version {APP_VERSION}, on Python {PYTHON_VERSION}) - Check for breached passwords with k-anonymity
Copyright (C) 2022  Sindastra <https://github.com/sindastra/passwnd>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License (version 3) for more details.
''')

if len(sys.argv) == 1:
    try:
        PASSWORD_PLAIN = getpass.getpass('Password to be checked (input is hidden): ').encode('UTF-8')
    except KeyboardInterrupt:
        exit('You force quit.')
    if not PASSWORD_PLAIN:
        exit('No password entered. Exiting.')
elif len(sys.argv) == 2:
    PASSWORD_PLAIN = sys.argv[1].encode('UTF-8')
else:
    exit('Please call this program either without arguments, or one password as argument.')

PASSWORD_HASHED = sha1(PASSWORD_PLAIN).hexdigest().upper()
HASH_PREFIX = PASSWORD_HASHED[:5]
HASH_SUFFIX = PASSWORD_HASHED[5:]

print(F'Submitting hash prefix: {HASH_PREFIX}...')

APIURL = 'https://api.pwnedpasswords.com/range/'
REQUEST = urllib.request.urlopen(APIURL + HASH_PREFIX)

if REQUEST.status != 200:
    exit('Unexpected server response.')

RESPONSE = REQUEST.read().decode()
RESULTS = RESPONSE.split()

print(F'Got {len(RESULTS)} hashes... Searching...')

FOUND = False

for ITEM in RESULTS:
    SEARCH = ITEM.split(':')
    PART = SEARCH[0]
    COUNT = SEARCH[1]
    if PART == HASH_SUFFIX:
        print(F'Password has been found {COUNT} times in breaches.')
        FOUND = True
        break

if not FOUND:
    print('No breach found.')

if os.name == 'nt':
    try:
        input('Press enter to exit.')
    except KeyboardInterrupt:
        exit()
