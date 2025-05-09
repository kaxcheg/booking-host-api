"""Initialization tests"""
import unittest

from booking_host_api.booking import Booking
from base.base import InvalidParameterError, AuthenticationError
from .common import BasicBookingTesting, write_private_data_to_file, get_OTP_from_input
from .common import some_not_registered_email, blocked_account_email, some_password, some_ses, some_auth_cookies, some_account_id

class TestBookingCredentialsInit(BasicBookingTesting):
    """
        Positive tests of initialization with Selenium.
        
        Provide json file ("tests/private_data.json" by default, see common.PRIVATE_DATA_FILE_PATH) with 
        valid email and password. See tests/private_data_template.json for structure of a private data file. 
        test_init_basic and test_init_otp, if succeeded, write ses, auth_cookies and account_id values to json file.
    """
    @classmethod
    def setUpClass(cls):
        cls.read_private_data_to_class('email', 'password')

    def test_init_basic(self):
        api = Booking(email=self.email, password=self.password)
        api.authenticate_and_setup()
        ses_value = api.access_ses()
        auth_cookies_value = api.access_auth_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, auth_cookies_value, account_id_value)
        write_private_data_to_file(ses=ses_value, auth_cookies=auth_cookies_value, account_id=account_id_value)
        
    def test_init_otp(self):
        api = Booking(email=self.email, password=self.password, OTP=get_OTP_from_input)
        api.authenticate_and_setup()
        ses_value = api.access_ses()
        auth_cookies_value = api.access_auth_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, auth_cookies_value, account_id_value)
        write_private_data_to_file(ses=ses_value, auth_cookies=auth_cookies_value, account_id=account_id_value)

    def test_init_with_account_id(self):
        api = Booking(email=self.email, password=self.password, account_id=some_account_id)
        api.authenticate_and_setup()
        ses_value = api.access_ses()
        auth_cookies_value = api.access_auth_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, auth_cookies_value, account_id_value)
        self.assertEqual(some_account_id, account_id_value, f'account_id was set to {account_id_value}, expected {some_account_id}')

    def test_init_otp_with_account_id(self):
        api = Booking(email=self.email, password=self.password, account_id=some_account_id, OTP=get_OTP_from_input)
        api.authenticate_and_setup()
        ses_value = api.access_ses()
        auth_cookies_value = api.access_auth_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, auth_cookies_value, account_id_value)
        self.assertEqual(some_account_id, account_id_value, f'account_id was set to {account_id_value}, expected {some_account_id}')


class TestBookingAuthDataInit(BasicBookingTesting):
    """Positive tests of initialization with auth data"""
    def test_init_with_auth_data(self):
        api = Booking(ses=some_ses, auth_cookies=some_auth_cookies, account_id=some_account_id)
        ses_value = api.access_ses()
        auth_cookies_value = api.access_auth_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, auth_cookies_value, account_id_value)
        self.assertEqual(some_ses, ses_value, f'ses was set to {ses_value}, expected {some_ses}')
        self.assertEqual(some_auth_cookies, auth_cookies_value, f'auth_cookies were set to {auth_cookies_value}, expected {some_auth_cookies}')
        self.assertEqual(some_account_id, account_id_value, f'account_id was set to {account_id_value}, expected {some_account_id}')

class TestBookingInitExceptions(unittest.TestCase):
    """Negative exceptive initialization tests"""
    def test_basic_init_exceptions(self):
        init_test_cases = [
            {
                "exception": InvalidParameterError,
                "init_kwargs": {},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR ses, auth_cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"email": some_not_registered_email},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR ses, auth_cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"password": some_password},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR ses, auth_cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"ses": some_ses, "auth_cookies": some_auth_cookies},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR ses, auth_cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"ses": some_ses, "account_id": some_account_id},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR ses, auth_cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"auth_cookies": some_auth_cookies, "account_id": some_account_id},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR ses, auth_cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"ses": '', "auth_cookies": some_auth_cookies, "account_id": some_account_id},
                "msg": "Wrong usage: ses cannot be blank."
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"ses": some_ses, "auth_cookies": some_auth_cookies, "account_id": 0},
                "msg": "Wrong usage: account_id cannot be blank."
            },
        ]

        for case in init_test_cases:
            with self.subTest(init_kwargs=case["init_kwargs"], exception=case["exception"]):
                self.assertRaisesRegex(case["exception"], case['msg'], Booking, **case["init_kwargs"])

    def test_basic_authorize_exceptions(self):
        authorize_test_cases = [
            {
                "exception": AuthenticationError,
                "init_kwargs": {"email": some_not_registered_email, "password": some_password},
                "msgs": ["Captcha detected.", "Wrong email."]
            },
            {
                "exception": AuthenticationError,
                "init_kwargs": {"email": blocked_account_email, "password": some_password},
                "msgs": ["Captcha detected.", "Account blocked."]
            },
        ]

        for case in authorize_test_cases:
            with self.subTest(init_kwargs=case["init_kwargs"], exception=case["exception"]):
                api = Booking(**case["init_kwargs"])
                with self.assertRaises(case["exception"]) as cm:
                    api.authenticate_and_setup()
                error_message = str(cm.exception)
                self.assertTrue(
                    any(expected_msg == error_message for expected_msg in case["msgs"]),
                    f"Error message '{error_message}' does not match any of expected: {case['msgs']}"
                )

if __name__ == "__main__":
    unittest.main()