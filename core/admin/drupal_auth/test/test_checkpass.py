import unittest

from drupal_auth.checkpassword import check_user_password, password_base64_encode


class CheckPassTestSuite(unittest.TestCase):
    """Tests for password comparisons"""

    def test_known_password(self):
        hashed = '$S$D4rHeM6Yb3Pqvr.3unYTA1xEOPazIsaIG5NdYOV..yN0UNC59TAz'
        self.assertTrue(check_user_password('testpwd', hashed))

    def test_empty_password(self):
        self.assertFalse(check_user_password('testpwd', None))
        self.assertFalse(check_user_password('testpwd', ''))

    def test_base64_encode(self):
        expected = '27LRk34'
        input = 'Drupal'
        self.assertEqual(password_base64_encode(input.encode('utf-8'), 5), expected)

    def test_sanity(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
