#!/usr/bin/env python2
from __future__ import print_function
import contextlib
import json
import sys
import traceback
from importlib import import_module
from math import ceil
from hashlib import sha512
from optparse import OptionParser

import os

default_config_file_path = "/etc/checkpassword.py.cfg.json"

itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def password_base64_encode(strin, count):
    output = ''
    i = 0
    while True:
        value = strin[i]
        i = i + 1
        output = output + itoa64[value & 0x3f]
        if i < count:
            value = value | strin[i] << 8
        output = output + itoa64[(value >> 6) & 0x3f]
        if i >= count:
            break
        i = i + 1
        if i < count:
            value = value | strin[i] << 16
        output = output + itoa64[(value >> 12) & 0x3f]
        if i >= count:
            break
        i = i + 1
        output = output + itoa64[(value >> 18) & 0x3f]
        if i >= count:
            break
    return output


def check_user_password(pwd, hashed):
    if hashed is None or hashed == '':
        return False

    setting = hashed[0:12]
    assert setting[0] == '$'
    assert setting[2] == '$'

    count_log2 = itoa64.find(setting[3])
    assert count_log2 >= 7
    assert count_log2 <= 30

    salt = setting[4:12]
    assert len(salt) == 8

    count = 1 << count_log2

    digest = sha512((salt + pwd).encode('utf-8')).digest()
    while True:
        digest = sha512(digest + pwd.encode('utf-8')).digest()
        count = count - 1
        if count == 0:
            break

    digest_length = len(digest)
    output = setting + password_base64_encode(digest, digest_length)
    expected = 12 + ceil((8 * digest_length) / 6.0)
    assert len(output) == expected

    computed = output[0:55]

    return computed == hashed


# noinspection SqlNoDataSourceInspection,SqlResolve
def query_password(username, connection_factory):
    """Query hashed password for a given user"""
    base_query = "SELECT pass FROM users WHERE name = "
    paramstyle = connection_factory.paramstyle
    if paramstyle == 'qmark':
        (query, params) = (base_query + '?', (username,))
    elif paramstyle == 'numeric':
        (query, params) = (base_query + ':1', (username,))
    elif paramstyle == 'named':
        (query, params) = (base_query + ':username', {username: username})
    elif paramstyle == 'format':
        (query, params) = (base_query + '%s', (username,))
    else:
        (query, params) = (base_query + '%(username)s', {username: username})
    with connection_factory.make() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if cursor.rowcount != 0:
            rows = cursor.fetchone()
            if rows is not None and len(rows) > 0 and rows[0] != '':
                return rows[0]
        return None


def load_config(path):
    return json.load(open(path, 'r'))


def default_config():
    if os.path.exists(default_config_file_path):
        return load_config(default_config_file_path)
    else:
        return {
            "module": "sqlite3",
            "options": {
                "database": ":memory:"
            }
        }


class ConfiguredConnectionFactory:

    def __init__(self, config=default_config()):
        self.module = import_module(config["module"])
        self.paramstyle = self.module.paramstyle
        self.options = config["options"]

    @contextlib.contextmanager
    def make(self):
        conn = self.module.connect(**self.options)
        try:
            yield conn
        finally:
            conn.close()


def read_input():
    with os.fdopen(3) as infile:
        data = infile.read(512).split('\0')
    return data


def main():
    usage = "usage %prog [options] cmd"
    parser = OptionParser(usage)
    parser.add_option("-f", "--config", dest="config", help="config file location")
    (options, args) = parser.parse_args()

    if len(args) == 0:
        print(usage, file=sys.stderr)
        print("Command missing", file=sys.stderr)
        return 2

    if options.config:
        config = options.config
    else:
        config = default_config_file_path

    try:
        (user, pwd) = read_input()[:2]
    except OSError as error:
        print('''%(error)s

Unable to read input from file descriptor 3.
Expecting data in format username\\0password\\0... on fd3.''' % locals(), file=sys.stderr)
        return 2

    conf = load_config(config)
    cf = ConfiguredConnectionFactory(conf)
    if conf.has_key('domain'):
        domain = conf['domain']
    else:
        domain = 'mailtest-cmi.e-bs.cz'
    if '@' not in user:
        (justuser, givenDomain) = (user, domain)
    else:
        (justuser, givenDomain) = user.split('@')
    if givenDomain != domain:
        return 1
    # Authenticate only users without domain explicitly specified
    if check_user_password(pwd, query_password(justuser, cf)):
        os.environ['USER'] = '%s@%s' % (justuser, domain)
        os.environ['HOME'] = '/mail/%s@%s' % (justuser, domain)
        os.environ['userdb_home'] = '/mail/%s@%s' % (justuser, domain)
        os.environ['userdb_uid'] = '8'
        os.environ['userdb_gid'] = '12'
        os.environ['INSECURE_SETUID'] = '1'
        os.environ['EXTRA'] = 'userdb_home userdb_uid userdb_gid'
        return os.execvp(args[0], args[0:])
    else:
        return 1


if __name__ == '__main__':
    try:
        result = main()
        if result is not None:
            sys.exit(result)
        else:
            sys.exit(111)
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(111)
