"""Tests the HumanizedByte functionality"""

import unittest

from unifierlib.utility import humanize_bytes, DEFAULT_SCALE
from unifierlib.utility import HumanizedByte

class TestHumanizeBytes(unittest.TestCase):
    """Tests the humanize-bytes functionality"""
    def test_hb_01(self):
        """Tests Basic Scaling"""
        tests = [
            {
                "test": 4,
                "expected": (4.0, 'B')
            },
            {
                "test": 4096,
                "expected": (4.0, 'KB')
            },
            {
                "test": 4194304,
                "expected": (4.0, 'MB')
            },
            {
                "test": 4294967296,
                "expected": (4.0, 'GB')
            },
            {
                "test": 4398046511104,
                "expected": (4.0, 'TB')
            },
            {
                "test": 4503599627370496,
                "expected": (4.0, 'PB')
            },
            {
                "test": 4611686018427387904,
                "expected": (4.0, 'EB')
            },
            {
                "test": 4722366482869645213696,
                "expected": (4.0, 'ZB')
            },
            {
                "test": 4835703278458516698824704,
                "expected": (4.0, 'YB')
            },
        ]
        for test in tests:
            test_val = test["test"]
            expected = test["expected"]
            with self.subTest(test_val=test_val, expected=expected):
                result = humanize_bytes(test_val)
                self.assertEqual(result, expected)

    def test_hb_02(self):
        """Tests over the end of the scale"""
        #What's after yotta, lotta? :D
        lotta = 4 * (1024 ** 9)
        expected = (lotta / DEFAULT_SCALE[0], "GB")
        result = humanize_bytes(lotta)
        self.assertEqual(result, expected)

    def test_hb_03(self):
        """Tests negative numbers"""
        tests = [
            {
                "test": -4,
                "expected": (-4.0, 'B')
            },
            {
                "test": -4 * 1024,
                "expected": (-4.0, 'KB')
            },
            {
                "test": -4 * 1024**2,
                "expected": (-4.0, 'MB')
            },
            {
                "test": -4 * 1024**3,
                "expected": (-4.0, 'GB')
            },
            {
                "test": -4 * 1024**4,
                "expected": (-4.0, 'TB')
            },
            {
                "test": -4 * 1024**5,
                "expected": (-4.0, 'PB')
            },
            {
                "test": -4 * 1024**6,
                "expected": (-4.0, 'EB')
            },
            {
                "test": -4 * 1024**7,
                "expected": (-4.0, 'ZB')
            },
            {
                "test": -4 * 1024**8,
                "expected": (-4.0, 'YB')
            },
        ]
        for test in tests:
            test_val = test["test"]
            expected = test["expected"]
            with self.subTest(test_val=test_val, expected=expected):
                result = humanize_bytes(test_val)
                self.assertEqual(result, expected)

    def test_hb_04(self):
        """Test the HumanizedBytes class"""
        tests = [
            {
                "raw": 4.0,
                "unit": 'B',
                "scaled": 4.0,
                "rounding": 2
            },
            {
                "raw": 4 * 1024,
                "unit": 'KB',
                "scaled": 4.0,
                "rounding": 2
            },
            {
                "raw": 4 * 1024**2,
                "unit": 'MB',
                "scaled": 4.0,
                "rounding": 2
            },
            {
                "raw": 4 * 1024**3,
                "unit": 'GB',
                "scaled": 4.0,
                "rounding": 2
            },
            {
                "raw": 4 * 1024**4,
                "unit": 'TB',
                "scaled": 4.0,
                "rounding": 2
            },
            {
                "raw": 4 * 1024**5,
                "unit": 'PB',
                "scaled": 4.0,
                "rounding": 2
            },
            {
                "raw": 4 * 1024**6,
                "unit": 'EB',
                "scaled": 4.0,
                "rounding": 2
            },
            {
                "raw": 4 * 1024**7,
                "unit": 'ZB',
                "scaled": 4.0,
                "rounding": 2
            },
            {
                "raw": 4 * 1024**8,
                "unit": 'YB',
                "scaled": 4.0,
                "rounding": 2
            },
            {
                "raw": 4 * 1024**9,
                "unit": 'GB',
                "scaled": (4*1024**9)/(1024**3),
                "rounding": 2
            },
        ]

        for test in tests:
            with self.subTest(test=test):
                raw = test["raw"]
                unit = test["unit"]
                scaled = test["scaled"]
                rounding = test.get("rounding", None)
                if not rounding:
                    rounding = 2
                fancy_s = f"{round(scaled, rounding)} {unit}"
                human_bytes = HumanizedByte(raw, rounding=rounding)
                self.assertEqual(scaled, human_bytes.size)
                self.assertEqual(raw, human_bytes.size_raw)
                self.assertEqual(unit, human_bytes.unit)
                self.assertEqual(fancy_s, human_bytes.size_str)
                self.assertEqual(fancy_s, str(human_bytes))
