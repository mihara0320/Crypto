import os
import crypto
import unittest

KEY = 'password'
CONTENT = "This is test"
c = crypto

class TestEncryption(unittest.TestCase):

    def test_encryption(self):
        with open('unit_test.txt', 'wb') as test_file:
            message = test_file.write(CONTENT)
            test_file.close()

        c.encrypt(c.get_key(KEY), os.getcwd(), 'unit_test.txt')
        self.assertNotEqual(CONTENT, message, "[-] Encryption Failed")
        try:
            os.remove('(encryted)unit_test.txt')
        except OSError:
            pass


    def test_decryption(self):
        with open('unit_test.txt', 'wb') as test_file:
            message = test_file.write(CONTENT)
            test_file.close()

        c.encrypt(c.get_key(KEY), os.getcwd(), 'unit_test.txt')
        c.decrypt(c.get_key(KEY), os.getcwd(), '(encryted)unit_test.txt')

        with open('unit_test.txt', 'rb') as test_file:
            message = test_file.read()
            test_file.close()

        self.assertEqual(CONTENT, message, "[-] Decryption Failed")
        try:
            os.remove('unit_test.txt')
        except OSError:
            pass
