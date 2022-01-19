#!/usr/bin/env python3
#
# passwnd - Check for breached passwords with k-anonymity
# Copyright (c) 2022 Sindastra <https://github.com/sindastra/passwnd>
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import getpass
import sys
from sys import exit  # This is for pyinstaller to work
from hashlib import sha1
import requests
import os

print('''passwnd - Check for breached passwords with k-anonymity
Copyright (c) 2022 Sindastra <https://github.com/sindastra/passwnd>
All rights reserved.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
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
REQUEST = requests.get(APIURL + HASH_PREFIX)

if REQUEST.status_code != 200:
    exit('Unexpected server response.')

RESPONSE = REQUEST.text.strip()
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
