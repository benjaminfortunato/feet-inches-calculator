# Unit Test Coverage for Feet & Inches Calculator

This document outlines the comprehensive unit test coverage for the Feet & Inches Calculator to ensure mathematical accuracy and prevent calculation errors.

## Test Suite Overview

The calculator includes **19 comprehensive test methods** covering all major functionality:

### 1. Parsing Tests (7 test methods)
- **test_parsing_feet_only**: Tests parsing of feet-only measurements (e.g., "5'")
- **test_parsing_inches_only**: Tests parsing of inches-only measurements (e.g., "11\"")
- **test_parsing_feet_and_inches**: Tests parsing of combined feet and inches (e.g., "5' 11\"")
- **test_parsing_pure_fractions**: Tests parsing of fractions without whole numbers (e.g., "1/2\"")
- **test_parsing_mixed_fractions_without_feet**: Tests parsing of mixed fractions (e.g., "0 1/2\"", "2 3/4\"")
- **test_parsing_feet_with_fractions**: Tests parsing of feet with fractional inches (e.g., "5' 7/8\"")
- **test_parsing_feet_with_mixed_fractions**: Tests parsing of feet with mixed fractional inches (e.g., "5' 11 7/8\"")

### 2. Arithmetic Operation Tests (5 test methods)
- **test_basic_addition**: Tests addition operations with various measurement formats
- **test_basic_subtraction**: Tests subtraction operations
- **test_multiplication**: Tests multiplication operations (e.g., "2' * 3")
- **test_division**: Tests division operations (e.g., "6' / 2")
- **test_negative_results**: Tests operations that result in negative values

### 3. Advanced Mathematical Tests (2 test methods)
- **test_pemdas_order_of_operations**: Tests proper order of operations (PEMDAS)
- **test_complex_expressions**: Tests multi-operation expressions with parentheses

### 4. Formatting Tests (2 test methods)
- **test_formatting_positive_results**: Tests proper formatting of positive results
- **test_formatting_negative_results**: Tests proper formatting of negative results

### 5. Edge Cases and Validation Tests (2 test methods)
- **test_edge_cases**: Tests boundary conditions and special cases
- **test_validation_errors**: Tests that invalid expressions raise appropriate errors

### 6. Real-World Application Test (1 test method)
- **test_real_world_scenarios**: Tests practical construction/measurement scenarios

## Build Process Integration

The unit tests are automatically executed during the build process:

1. **Pre-Build Testing**: The `build.py` script runs all unit tests before creating the executable
2. **Build Failure on Test Failure**: If any test fails, the build process is aborted
3. **Test Success Confirmation**: Only proceeds to build the executable if all tests pass

## Test Coverage Areas

### Measurement Formats Tested:
- Feet only: `5'`
- Inches only: `11"`
- Feet and inches: `5' 11"`
- Pure fractions: `1/2"`, `7/8"`
- Mixed fractions: `0 1/2"`, `2 3/4"`
- Feet with fractions: `5' 7/8"`
- Feet with mixed fractions: `5' 11 7/8"`

### Mathematical Operations Tested:
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Order of operations (PEMDAS)
- Parentheses grouping
- Complex multi-operation expressions

### Error Conditions Tested:
- Invalid input formats
- Missing measurement designations
- Malformed expressions
- Division by zero scenarios

### Precision and Accuracy:
- All tests use `assertAlmostEqual` with 6 decimal places precision
- Tests cover fractional calculations down to 1/64 inch precision
- Negative result handling and formatting
- Zero result handling

## Running Tests

### Manual Test Execution:
```bash
python test_calculator.py
```

### GUI Test Execution:
- Click the "Run Tests" button in the calculator application
- Results are displayed in a popup window

### Build Process Test Execution:
```bash
python build.py
```
Tests run automatically before building the executable.

## Test Results

When all tests pass, you'll see:
```
Ran 19 tests in [time]s

OK

ALL TESTS PASSED! Calculator is working correctly.
```

This comprehensive test suite ensures that:
- All measurement parsing is mathematically correct
- All arithmetic operations follow proper mathematical rules
- Edge cases are handled appropriately
- User input validation works correctly
- The calculator produces accurate results for real-world scenarios

The tests provide confidence that there are no basic mathematical errors in the calculator implementation.
