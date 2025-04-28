import json
import unittest

from base.tests.common import (
    write_private_data_to_file, read_private_data, compare_dicts, get_OTP_from_input, 
    PRIVATE_DATA_FILE_PATH)

import booking_host_api.booking_locators as locators

some_not_registered_email = 'non_registered@e.mail'
blocked_account_email = 'email@gmail.com'
some_password = 'pass'
some_ses = 'some_ses'
some_auth_cookies = {cookie_name: 'some_value' for cookie_name in locators.auth_cookie_names}
some_account_id = 12345678
some_property_id = 12345678

class BasicBookingTesting(unittest.TestCase):
    @classmethod
    def read_private_data_to_class(cls, *args):
        with open(PRIVATE_DATA_FILE_PATH, "r") as f:
                secrets = json.load(f)

        for arg in args:
             setattr(cls, arg, secrets[arg])
 
    def basic_assert_auth_data(self, ses_value, auth_cookies_value, account_id_value):  
        self.assertTrue(ses_value, "ses should not be blank")
        self.assertTrue(auth_cookies_value, "auth_cookies should not be blank")
        self.assertTrue(account_id_value, "account_id should not be blank")
        self.assertIsInstance(ses_value, str, "ses should be a string")
        self.assertIsInstance(auth_cookies_value, dict, "auth_cookies should be a dict")
        self.assertIsInstance(account_id_value, int, "account_id should be an integer")