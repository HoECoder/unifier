"""Tests the HumanizedByte functionality"""

import unittest

from unifierlib.utility import reorganize_site_data

class TestReorgSiteData(unittest.TestCase):
    """Tests the reorganize_site_data utility function"""
    def test_rs_01(self):
        """Tests a None for data"""
        self.assertIsNone(reorganize_site_data(None))

    def test_rs_02(self):
        """Tests invalid "data" blocks"""
        tests = [
            {
                "test": {},
                "result": None
            },
            {
                "test": {"thing": 5},
                "result": {"thing": 5}
            },
            {
                "test": {"another thing": 5},
                "result": {"another thing": 5}
            }
        ]
        for test in tests:
            test_val = test["test"]
            expected = test["result"]
            with self.subTest(test=test):
                self.assertEqual(expected, reorganize_site_data(test_val))

    def test_rs_03(self):
        """Tests Various meta dicts"""
        tests = [
            {
                "test": {"meta": "thing"},
                "result": {"meta": "thing"}
            },
            {
                "test": {"meta": {}},
                "result": {"meta": {}}
            },
            {
                "test": {"meta": {"rc": "ok"}},
                "result": {"meta": {"rc": "ok"}}
            },
            {
                "test": {
                    "meta": {"rc": "ok"},
                    "data": {}
                },
                "result": {}
            },
            {
                "test": {
                    "meta": {"rc": "ok"},
                    "data": []
                },
                "result": {}
            },
            {
                "test": {
                    "meta": {"rc": "nok"},
                    "data": []
                },
                "result": {
                    "meta": {"rc": "nok"},
                    "data": []
                }
            },
            {
                "test": {
                    "meta": {"rc": "nok"},
                    "data": [
                        {},
                        {},
                        {}
                    ]
                },
                "result": {
                    "meta": {"rc": "nok"},
                    "data": [
                        {},
                        {},
                        {}
                    ]
                },
            },
        ]
        for test in tests:
            with self.subTest(test=test):
                expected = test["result"]
                test_val = test["test"]
                result = reorganize_site_data(test_val)
                self.assertEqual(expected,
                                 result)

    def test_rs_04(self):
        """Tests various re-orginizations"""
        tests = [
            {
                "test": {
                    "meta": {"rc": "ok"},
                    "data": [
                        {},
                        {},
                        {}
                    ]
                },
                "result": {}
            },
            {
                "test": {
                    "meta": {"rc": "ok"},
                    "data": [
                        {
                            "name": "bob",
                            "stuff": [1, 2, 3]
                        },
                        {
                            "name": "bill"
                        },
                        {
                            "nam": "frank",
                            "stuff": [1, 2, 3]
                        }
                    ]
                },
                "result": {
                    "bob": {
                        "name": "bob",
                        "stuff": [1, 2, 3]
                    },
                    "bill": {
                        "name": "bill"
                    }
                }
            },
        ]
        for test in tests:
            with self.subTest(test=test):
                expected = test["result"]
                test_val = test["test"]
                result = reorganize_site_data(test_val)
                self.assertEqual(expected,
                                 result)
