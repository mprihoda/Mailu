import json
import unittest

from drupal_auth.checkpassword import ConfiguredConnectionFactory


class ConnectionFactoryTestSuite(unittest.TestCase):
    '''Connection factory tests'''

    def test_configured_connection_factory(self):
        sample_config = '''
{
    "module": "sqlite3",
    "options": {
        "database": ":memory:"
    }
}
        '''
        with ConfiguredConnectionFactory(json.loads(sample_config)).make() as conn:
            cursor = conn.cursor()
            # noinspection SqlNoDataSourceInspection
            cursor.execute("SELECT 1 AS a")
            cursor.close()


if __name__ == '__main__':
    unittest.main()
