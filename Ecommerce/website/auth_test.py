import unittest   # The test framework
from website import auth_functions
from passlib.hash import sha256_crypt

class Test_HashUserPassword(unittest.TestCase):

    def test_correct_lenght_for_short_password(self):
        self.assertEqual(len(auth_functions.hash_User_Password("1234")), 77)
        self.assertEqual(len(auth_functions.hash_User_Password("1")), 77)
    
    def test_correct_hash_lenght_for_large_password(self):
        self.assertEqual(len(auth_functions.hash_User_Password("thisIsAnExamplePassword1234")), 77)
        self.assertEqual(len(auth_functions.hash_User_Password("thisIsAnExamplePasswordThatIsLarger")), 77)
    
    def test_hash_functions_is_properly_hashing(self):
        password1 = auth_functions.hash_User_Password("1234")
        password2 = auth_functions.hash_User_Password("ThisOnlyContainsCharAnd4738628")
        password3 = auth_functions.hash_User_Password("ThisContains1234!@#$%^&**")

        self.assertTrue(sha256_crypt.verify("1234", password1))
        self.assertTrue(sha256_crypt.verify("ThisOnlyContainsCharAnd4738628", password2))
        self.assertTrue(sha256_crypt.verify("ThisContains1234!@#$%^&**", password3))

    def test_same_password_hash_differ(self):

        password1 = auth_functions.hash_User_Password("1234")
        password2 = auth_functions.hash_User_Password("12345678")
        password3 = auth_functions.hash_User_Password("FPUFPU")

        self.assertNotEqual(auth_functions.hash_User_Password("1234"), password1)
        self.assertNotEqual(auth_functions.hash_User_Password("12345678"), password2)
        self.assertNotEqual(auth_functions.hash_User_Password("FPUFPU"), password3 )

class Test_VerifyUserPassword(unittest.TestCase):

    def test_passwords_match(self):
        self.assertTrue(auth_functions.verify_User_Password("1234", sha256_crypt.encrypt("1234")))
    
    def test_passwords_dont_match(self):
        self.assertFalse(auth_functions.verify_User_Password("1234", sha256_crypt.encrypt("12345678")))
        


if __name__ == '__main__':
    unittest.main()