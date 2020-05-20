"""Tests the Controller functionality"""

import unittest
from unittest.mock import patch, MagicMock
import io

from requests import Session, Response, ConnectionError

from unifierlib import Controller

#pylint: disable=line-too-long

class MockResponse:
    def __init__(self, status_code, url, text):
        self.status_code = status_code
        self.url = url
        self.raw = io.StringIO(text)
    def __bool__(self):
        return self.ok
    @property
    def ok(self):
        if 400 <= self.status_code < 600:
            return False
        return True
    def close(self):
        return True

class TestController(unittest.TestCase):
    """D"""
    def setUp(self):
        pass
    @patch('requests.Session.post')
    def test_cont_01(self, mock_post: MagicMock):
        """Test Bad Credentials"""
        host = 'localhost'
        port = 8443
        mock_post.return_value = MockResponse(400,
                                              f"https://{host}:{port}/api/login",
                                              '{"meta":{"rc":"error","msg":"api.err.Invalid"},"data":[]}')
        user = 'test'
        password = 'password'
        controller = Controller(host, port, user, password)
        res = controller.logged_in
        self.assertFalse(res)
    @patch('requests.Session.post')
    def test_cont_02(self, mock_post: MagicMock):
        """Tests A Connection is Refused"""
        mock_post.side_effect = ConnectionError()
        host = 'localhost'
        port = 8443
        user = 'test'
        password = 'password'
        with self.assertRaises(ConnectionError):
            #pylint: disable=unused-variable
            controller = Controller(host, port, user, password)

    @patch('requests.Session.post')
    def test_cont_03(self, mock_post: MagicMock):
        """Tests Good Connection"""
        host = 'localhost'
        port = 8443
        user = 'test'
        password = 'password'
        mock_post.return_value = MockResponse(200,
                                              f"https://{host}:{port}/api/login",
                                              '{"meta":{"rc":"ok"},"data":[]}')
        controller = Controller(host, port, user, password)
        res = controller.logged_in
        self.assertTrue(res)
    @patch('requests.Session.post')
    def test_cont_04(self, mock_post: MagicMock):
        """Test stat methods return None when not logged in"""
        host = 'localhost'
        port = 8443
        mock_post.return_value = MockResponse(400,
                                              f"https://{host}:{port}/api/login",
                                              '{"meta":{"rc":"error","msg":"api.err.Invalid"},"data":[]}')
        user = 'test'
        password = 'password'
        controller = Controller(host, port, user, password)
        res = controller.logged_in
        self.assertFalse(res)
        test_methods = [
            controller.get_daily_stats,
            controller.get_hourly_stats,
            controller.get_minutely_stats,
            controller.site_info_detailed,
            controller.site_info_simplified
        ]
        for test_method in test_methods:
            with self.subTest(test_method=test_method):
                res = test_method()
                self.assertIsNone(res)
