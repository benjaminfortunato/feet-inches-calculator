#!/usr/bin/env python3
"""
Comprehensive unit tests for the Feet and Inches Calculator
This file contains all tests to ensure mathematical accuracy and proper formatting.
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import calculator_engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculator_engine import FeetInchesCalculator


class TestFeetInchesCalculator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = FeetInchesCalculator()

    def test_parsing_feet_only(self):
        """Test parsing feet-only measurements"""
        test_cases = [
            ("1'", 12.0),
            ("5'", 60.0),
            ("10'", 120.0),
            ("0'", 0.0),
        ]
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                result = self.calc.parse_measurement(input_str)
                self.assertAlmostEqual(result, expected, places=6)

    def test_parsing_inches_only(self):
        """Test parsing inches-only measurements"""
        test_cases = [
            ('1"', 1.0),
            ('12"', 12.0),
            ('6.5"', 6.5),
            ('0"', 0.0),
        ]
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                result = self.calc.parse_measurement(input_str)
                self.assertAlmostEqual(result, expected, places=6)

    def test_parsing_feet_and_inches(self):
        """Test parsing feet and inches combinations"""
        test_cases = [
            ("1' 6\"", 18.0),
            ("2' 3\"", 27.0),
            ("5' 11\"", 71.0),
            ("0' 6\"", 6.0),
            ("10' 0\"", 120.0),
        ]
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                result = self.calc.parse_measurement(input_str)
                self.assertAlmostEqual(result, expected, places=6)

    def test_parsing_pure_fractions(self):
        """Test parsing pure fractions"""
        test_cases = [
            ('1/2"', 0.5),
            ('1/4"', 0.25),
            ('3/4"', 0.75),
            ('1/8"', 0.125),
            ('3/8"', 0.375),
            ('5/8"', 0.625),
            ('7/8"', 0.875),
            ('1/16"', 0.0625),
            ('15/16"', 0.9375),
            ('1/32"', 0.03125),
        ]
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                result = self.calc.parse_measurement(input_str)
                self.assertAlmostEqual(result, expected, places=6)

    def test_parsing_mixed_fractions_without_feet(self):
        """Test parsing mixed fractions without feet (0 1/2" format)"""
        test_cases = [
            ('0 1/2"', 0.5),
            ('1 1/2"', 1.5),
            ('2 3/4"', 2.75),
            ('5 7/8"', 5.875),
            ('11 15/16"', 11.9375),
            ('0 1/4"', 0.25),
            ('0 3/8"', 0.375),
        ]
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                result = self.calc.parse_measurement(input_str)
                self.assertAlmostEqual(result, expected, places=6)

    def test_parsing_feet_with_fractions(self):
        """Test parsing feet with fraction inches"""
        test_cases = [
            ("1' 1/2\"", 12.5),
            ("2' 3/4\"", 24.75),
            ("5' 7/8\"", 60.875),  # 5*12 + 7/8 = 60 + 0.875
            ("10' 11/16\"", 120.6875),  # 10*12 + 11/16 = 120 + 0.6875
            ("0' 1/4\"", 0.25),
        ]
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                result = self.calc.parse_measurement(input_str)
                self.assertAlmostEqual(result, expected, places=6)

    def test_parsing_feet_with_mixed_fractions(self):
        """Test parsing feet with mixed fraction inches"""
        test_cases = [
            ("1' 2 3/4\"", 14.75),
            ("2' 1 1/2\"", 25.5),
            ("5' 11 7/8\"", 71.875),  # 5*12 + 11 + 7/8 = 60 + 11 + 0.875
            ("10' 5 1/16\"", 125.0625),
        ]
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                result = self.calc.parse_measurement(input_str)
                self.assertAlmostEqual(result, expected, places=6)

    def test_basic_addition(self):
        """Test basic addition operations"""
        test_cases = [
            ("1' + 1'", 24.0),
            ('6" + 6"', 12.0),
            ("1' + 6\"", 18.0),
            ('1/2" + 1/2"', 1.0),
            ("1' 6\" + 2' 3\"", 45.0),
        ]
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.evaluate_expression(expression)
                self.assertAlmostEqual(result, expected, places=6)

    def test_basic_subtraction(self):
        """Test basic subtraction operations"""
        test_cases = [
            ("2' - 1'", 12.0),
            ('12" - 6"', 6.0),
            ("1' 6\" - 6\"", 12.0),
            ('3/4" - 1/4"', 0.5),
            ("2' 3\" - 1' 6\"", 9.0),
        ]
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.evaluate_expression(expression)
                self.assertAlmostEqual(result, expected, places=6)

    def test_negative_results(self):
        """Test operations that result in negative values"""
        test_cases = [
            ("1' - 2'", -12.0),
            ('6" - 12"', -6.0),
            ('1/4" - 3/4"', -0.5),
            ('2" + 0 1/2" - 3"', -0.5),  # The original problematic case
            ("1' 6\" - 1' 8\"", -2.0),
        ]
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.evaluate_expression(expression)
                self.assertAlmostEqual(result, expected, places=6)

    def test_multiplication(self):
        """Test multiplication operations"""
        test_cases = [
            ("2' * 2", 48.0),
            ('6" * 3', 18.0),
            ('1/2" * 4', 2.0),
            ("1' 6\" * 2", 36.0),
        ]
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.evaluate_expression(expression)
                self.assertAlmostEqual(result, expected, places=6)

    def test_division(self):
        """Test division operations"""
        test_cases = [
            ("2' / 2", 12.0),
            ('12" / 3', 4.0),
            ('3/4" / 3', 0.25),
            ("3' / 2", 18.0),
        ]
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.evaluate_expression(expression)
                self.assertAlmostEqual(result, expected, places=6)

    def test_pemdas_order_of_operations(self):
        """Test PEMDAS (order of operations)"""
        test_cases = [
            ("1' + 2' * 2", 60.0),  # 12 + (24 * 2) = 60
            ('6" + 3" * 2', 12.0),  # 6 + (3 * 2) = 12
            ("(1' + 2') * 2", 72.0),  # (12 + 24) * 2 = 72
            ("2' * 3 + 1'", 84.0),  # (24 * 3) + 12 = 84
        ]
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.evaluate_expression(expression)
                self.assertAlmostEqual(result, expected, places=6)

    def test_complex_expressions(self):
        """Test complex multi-operation expressions"""
        test_cases = [
            ("1' 6\" + 2' 3\" - 1'", 33.0),  # 18 + 27 - 12 = 33
            ('1/2" + 1/4" + 1/8"', 0.875),  # 0.5 + 0.25 + 0.125 = 0.875
            ("2' * 2 + 6\"", 54.0),  # 24 * 2 + 6 = 54
            ("(1' + 6\") / 2", 9.0),  # (12 + 6) / 2 = 9
        ]
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.evaluate_expression(expression)
                self.assertAlmostEqual(result, expected, places=6)

    def test_formatting_positive_results(self):
        """Test formatting positive results"""
        test_cases = [
            (0.0, '0"'),
            (0.5, '1/2"'),
            (1.0, '1"'),
            (1.5, '1 1/2"'),
            (12.0, "1'"),
            (12.5, "1' 1/2\""),
            (18.75, "1' 6 3/4\""),
            (24.0, "2'"),
        ]
        for inches, expected in test_cases:
            with self.subTest(inches=inches):
                result = self.calc.format_result(inches)
                self.assertEqual(result, expected)

    def test_formatting_negative_results(self):
        """Test formatting negative results"""
        test_cases = [
            (-0.5, '-1/2"'),
            (-1.0, '-1"'),
            (-1.5, '-1 1/2"'),
            (-12.0, "-1'"),
            (-12.5, "-1' 1/2\""),
            (-18.75, "-1' 6 3/4\""),
            (-24.0, "-2'"),
        ]
        for inches, expected in test_cases:
            with self.subTest(inches=inches):
                result = self.calc.format_result(inches)
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        test_cases = [
            ("0' + 0\"", 0.0),
            ('0" - 0"', 0.0),
            ("100' + 0\"", 1200.0),
            ('1/64" + 1/64"', 0.03125),
            ("0' 0 1/64\"", 0.015625),
        ]
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.evaluate_expression(expression)
                self.assertAlmostEqual(result, expected, places=6)

    def test_validation_errors(self):
        """Test that invalid expressions raise appropriate errors"""
        invalid_expressions = [
            "10 11",  # Missing quotes
            "1' 2 3",  # Missing fraction denominator and quotes
            "abc",  # Non-numeric
            "1' +",  # Incomplete expression
            "/ 2'",  # Invalid start
        ]
        for expression in invalid_expressions:
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    self.calc.evaluate_expression(expression)

    def test_real_world_scenarios(self):
        """Test real-world construction/measurement scenarios"""
        test_cases = [
            # Adding lumber lengths: 2'6" + 1'8" + 3'2" = 30+20+38 = 88
            ("2' 6\" + 1' 8\" + 3' 2\"", 88.0),
            # Subtracting cut lengths: 8' - 2'3" = 96 - 27 = 69
            ("8' - 2' 3\"", 69.0),
            # Room perimeter: 12'6" + 10'3" + 12'6" + 10'3" = 150+123+150+123 = 546
            ("12' 6\" + 10' 3\" + 12' 6\" + 10' 3\"", 546.0),
            # Framing calculations: 16' - 2 * 1 1/2" = 192 - 3 = 189
            ("16' - 2 * 1 1/2\"", 189.0),
        ]
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result = self.calc.evaluate_expression(expression)
                self.assertAlmostEqual(result, expected, places=6)


def run_tests():
    """Run all tests and return success status"""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFeetInchesCalculator)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Return True if all tests passed
    return result.wasSuccessful()


def run_tests_silent():
    """Run all tests silently and return (success, failure_count, total_count)"""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFeetInchesCalculator)
    
    # Run the tests silently
    runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
    result = runner.run(suite)
    
    return result.wasSuccessful(), len(result.failures) + len(result.errors), result.testsRun


if __name__ == '__main__':
    print("Running Feet and Inches Calculator Unit Tests")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n" + "=" * 50)
        print("ALL TESTS PASSED! Calculator is working correctly.")
    else:
        print("\n" + "=" * 50)
        print("SOME TESTS FAILED! Please review the calculator implementation.")
        sys.exit(1)
