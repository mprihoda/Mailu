import contextlib
import sqlite3
import unittest
from drupal_auth.checkpassword import query_password

valid_users = [
    ('testuser', '$S$D4rHeM6Yb3Pqvr.3unYTA1xEOPazIsaIG5NdYOV..yN0UNC59TAz'),
    ('anotheruser', '$S$DD7BWIOu2YDNWRJ7wcGFdUN2DbuBunEN56EaqCHXRY7d3Ccu.Ucd'),
]

class FakeConnectionFactory:

    def __init__(self):
        self.paramstyle = sqlite3.paramstyle
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("CREATE TABLE users (name VARCHAR(255) NOT NULL PRIMARY KEY, pass VARCHAR(255))")
        self.conn.executemany("INSERT INTO users VALUES (?, ?)", valid_users)
        self.conn.commit()

    @contextlib.contextmanager
    def make(self):
        yield self.conn


# noinspection SqlNoDataSourceInspection,SqlResolve
class PasswordQueryTestSuite(unittest.TestCase):
    """Tests for password querying"""

    def test_obtain_password_for_valid_user(self):
        for (user, password) in valid_users:
            self.assertEqual(query_password(user, FakeConnectionFactory()), password)

    def test_no_password_for_missing_user(self):
        self.assertEqual(query_password('nouserhere', FakeConnectionFactory()), None)


if __name__ == '__main__':
    unittest.main()
