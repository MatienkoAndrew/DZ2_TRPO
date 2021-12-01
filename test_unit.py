# import unittest
# # from src.for_test import factorial
# from src.TransactionScript.Main import factorial
# 
class TestFactorial(unittest.TestCase):

    def test_calculation(self):
        self.assertEqual(3, factorial(2))

    def test_negative(self):
        self.assertRaises(ValueError, factorial, -1)

    def test_float(self):
        self.assertRaises(TypeError, factorial, 1.25)

    def test_zero(self):
        self.assertEqual(1, factorial(0))

import unittest

import psycopg2
from contextlib import closing

from src.TransactionScript.Main import User, factorial



class TestStringMethods123132(unittest.TestCase):

    def test_good_login(self):
        self.assertEqual(1, User('Andrew', '123').check_login())

    def test_bad_login(self):
        self.assertEqual(User('Andrew1421532', '123').check_login(), 'Wrong login')

    def test_good_password(self):
        self.assertEqual(User('Andrew', '123').check_password(), 1)

    def test_bad_password(self):
        self.assertEqual(User('Andrew', '1').check_password(), 'Wrong password')

# if __name__ == '__main__':
#     unittest.main()