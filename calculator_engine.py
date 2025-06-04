import re
from fractions import Fraction

class FeetInchesCalculator:
    def __init__(self):
        pass

    def parse_measurement(self, text: str) -> float:
        """Parse a measurement string and return total inches as float"""
        text = text.strip()
        
        # Check for feet with mixed number inches (e.g., "1' 2 3/4"")
        match = re.match(r"(\d+)'\s*(\d+)\s+(\d+)/(\d+)\"", text)
        if match:
            feet = int(match.group(1))
            whole_inches = int(match.group(2))
            numerator = int(match.group(3))
            denominator = int(match.group(4))
            fraction_inches = float(Fraction(numerator, denominator))
            return feet * 12 + whole_inches + fraction_inches
        
        # Check for feet with pure fraction inches (e.g., "1' 11/32"")
        match = re.match(r"(\d+)'\s*(\d+)/(\d+)\"", text)
        if match:
            feet = int(match.group(1))
            numerator = int(match.group(2))
            denominator = int(match.group(3))
            fraction_inches = float(Fraction(numerator, denominator))
            return feet * 12 + fraction_inches
        
        # Check for feet and inches (e.g., "1' 11"")
        match = re.match(r"(\d+)'\s*(\d+(?:\.\d+)?)\"", text)
        if match:
            feet = int(match.group(1))
            inches = float(match.group(2))
            return feet * 12 + inches
        
        # Check for feet only (e.g., "1'")
        match = re.match(r"(\d+)'$", text)
        if match:
            feet = int(match.group(1))
            return feet * 12
        
        # Check for mixed number inches without feet (e.g., "0 1/2"" or "2 3/4"")
        match = re.match(r"^(\d+)\s+(\d+)/(\d+)\"?$", text)
        if match:
            whole_inches = int(match.group(1))
            numerator = int(match.group(2))
            denominator = int(match.group(3))
            fraction_inches = float(Fraction(numerator, denominator))
            return whole_inches + fraction_inches
        
        # Check for pure fractions (e.g., "1/32"" or "1/32")
        match = re.match(r"^(\d+)/(\d+)\"?$", text)
        if match:
            numerator = int(match.group(1))
            denominator = int(match.group(2))
            return float(Fraction(numerator, denominator))
        
        # Check for inches only (e.g., "11.5"")
        match = re.match(r"^(\d+(?:\.\d+)?)\"$", text)
        if match:
            return float(match.group(1))
          # Plain number
        try:
            return float(text)
        except ValueError:
            raise ValueError(f"Unable to parse measurement: {text}")

    def format_result(self, total_inches: float, round_to: str = None) -> str:
        """Format total inches back to feet and inches with fractions"""
        # Handle negative values properly
        is_negative = total_inches < 0
        abs_inches = abs(total_inches)
        
        feet = int(abs_inches // 12)
        remaining_inches = abs_inches % 12
        
        if remaining_inches == 0:
            if feet == 0:
                return '0"'
            result = f"{feet}'"
            return f"-{result}" if is_negative else result
        
        # Convert decimal inches to fraction
        inches_fraction = Fraction(remaining_inches).limit_denominator(64)
        
        result_parts = []
        if feet > 0:
            result_parts.append(f"{feet}'")        
        whole_part = inches_fraction.numerator // inches_fraction.denominator
        remainder = inches_fraction.numerator % inches_fraction.denominator
        
        if remainder == 0:
            if whole_part > 0:
                result_parts.append(f'{whole_part}"')
        else:
            if whole_part > 0:
                result_parts.append(f'{whole_part} {remainder}/{inches_fraction.denominator}"')
            else:
                result_parts.append(f'{remainder}/{inches_fraction.denominator}"')
        
        result = ' '.join(result_parts) if result_parts else '0"'
        return f"-{result}" if is_negative else result

    def validate_expression(self, expression: str) -> tuple[bool, str]:
        """Validate expression format and return (is_valid, error_message)"""
        # Create a copy to work with
        temp_expr = expression
        
        # First, temporarily replace valid patterns to avoid false positives
        # Replace mixed fractions (0 1/2", 2 3/4", etc.)
        temp_expr = re.sub(r'\b\d+\s+\d+/\d+\"', ' VALID_MIXED ', temp_expr)
        
        # Replace feet with mixed fractions (1' 2 3/4")
        temp_expr = re.sub(r'\b\d+\'\s*\d+\s+\d+/\d+\"', ' VALID_FEET_MIXED ', temp_expr)
        
        # Replace feet with fractions (1' 3/4")
        temp_expr = re.sub(r'\b\d+\'\s*\d+/\d+\"', ' VALID_FEET_FRAC ', temp_expr)
        
        # Replace feet with inches (1' 11")
        temp_expr = re.sub(r'\b\d+\'\s*\d+\"', ' VALID_FEET_INCH ', temp_expr)
        
        # Replace feet only (1')
        temp_expr = re.sub(r'\b\d+\'', ' VALID_FEET ', temp_expr)
        
        # Replace pure fractions (1/2")
        temp_expr = re.sub(r'\b\d+/\d+\"', ' VALID_FRAC ', temp_expr)
        
        # Replace inches only (11")
        temp_expr = re.sub(r'\b\d+\"', ' VALID_INCH ', temp_expr)
        
        # Replace decimal numbers and integers that are used in mathematical operations
        # These are valid when used for multiplication, division, or as operands
        temp_expr = re.sub(r'[\*/]\s*\d+(?:\.\d+)?\b', ' * VALID_NUMBER ', temp_expr)
        temp_expr = re.sub(r'\b\d+(?:\.\d+)?\s*[\*/]', ' VALID_NUMBER * ', temp_expr)
        temp_expr = re.sub(r'[\+\-]\s*\d+(?:\.\d+)?\s*[\*/]', ' + VALID_NUMBER * ', temp_expr)
        temp_expr = re.sub(r'[\*/]\s*\d+(?:\.\d+)?\s*[\+\-]', ' * VALID_NUMBER + ', temp_expr)
        
        # Now check for problematic patterns in the cleaned expression
        
        # Check for numbers without any unit designation that are NOT part of valid operations
        number_without_unit = re.search(r'\b\d+\b(?!\s*[\'\"\/])', temp_expr)
        if number_without_unit:
            number = number_without_unit.group()
            # Only flag this as an error if it's not "VALID_NUMBER" (our placeholder)
            if number != "VALID_NUMBER":
                return False, f"Found number '{number}' without feet (') or inches (\") designation. Example: 10' 2 1/2\""
        
        # Check for fractions without quotes in the original expression
        # But first exclude cases where the fraction is already part of a valid pattern
        temp_check = expression
        
        # Remove all valid quoted fractions first
        temp_check = re.sub(r'\d+/\d+\"', '', temp_check)
        
        # Now look for any remaining fractions without quotes
        fraction_without_quote = re.search(r'\b\d+/\d+\b', temp_check)
        if fraction_without_quote:
            fraction = fraction_without_quote.group()
            return False, f"Found fraction '{fraction}' without inches (\") designation. Example: {fraction}\""
        
        return True, ""

    def evaluate_expression(self, expression: str) -> float:
        """Evaluate a mathematical expression with feet and inches measurements"""
        expression = expression.strip()
        
        # First validate the expression format
        is_valid, error_msg = self.validate_expression(expression)
        if not is_valid:
            raise ValueError(f"Format Error: {error_msg}")
        
        # Find all measurements and replace with inches
        measurements = self._extract_measurements(expression)
        processed_expression = expression
        
        # Sort measurements by length (longest first) to avoid partial replacements
        sorted_measurements = sorted(measurements.items(), key=lambda x: len(x[0]), reverse=True)
        
        for measurement, inches_value in sorted_measurements:
            processed_expression = processed_expression.replace(measurement, str(inches_value))
        
        # Replace common operators
        processed_expression = processed_expression.replace('x', '*')
        processed_expression = processed_expression.replace('X', '*')
        processed_expression = processed_expression.replace('÷', '/')
        
        try:
            result = eval(processed_expression)
            return float(result)
        except Exception as e:
            # Provide more helpful error messages
            if "invalid syntax" in str(e):
                return self._handle_syntax_error(expression, processed_expression)
            else:
                raise ValueError(f"Calculation Error: {str(e)}. Please check your expression format.")

    def _handle_syntax_error(self, original_expr: str, processed_expr: str):
        """Handle syntax errors with helpful messages"""
        # Common issues that cause syntax errors
        if re.search(r'\d+\s+\d+', original_expr):
            raise ValueError("Format Error: Make sure measurements follow the format 10' 2 1/2\". Are you missing a ' or \" designation?")
        
        if "  " in processed_expr:
            raise ValueError("Format Error: Invalid spacing in expression. Make sure measurements follow the format 10' 2 1/2\".")
        
        # Check for unmatched parentheses
        if processed_expr.count('(') != processed_expr.count(')'):
            raise ValueError("Format Error: Unmatched parentheses in expression.")
        
        # Generic syntax error
        raise ValueError("Format Error: Invalid expression format. Make sure measurements follow the format 10' 2 1/2\". Are you missing a ' or \" designation?")

    def _extract_measurements(self, expression: str) -> dict:
        """Extract all measurements from expression and convert to inches"""
        measurements = {}
        
        # Process from most specific to least specific to avoid partial matches
        temp_expression = expression
        
        # First pass: feet with mixed fractions (e.g., "1' 2 3/4"")
        matches = re.findall(r"\d+'\s*\d+\s+\d+/\d+\"", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Second pass: mixed numbers without feet (e.g., "0 1/2"")
        matches = re.findall(r"(?<!['\d])\d+\s+\d+/\d+\"", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Third pass: feet with fractions
        matches = re.findall(r"\d+'\s*\d+/\d+\"", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Fourth pass: feet with inches
        matches = re.findall(r"\d+'\s*\d+\"", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Fifth pass: feet only
        matches = re.findall(r"\d+'(?=\s|$|[+\-*/()])", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Sixth pass: pure fractions with quotes
        matches = re.findall(r"(?<!['\d])\d+/\d+\"", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Seventh pass: inches only
        matches = re.findall(r"(?<!['\d])\d+\"", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
        
        return measurements

    def _round_to_fraction(self, value: float, round_to_str: str) -> float:
        """Round value to the nearest specified fraction"""
        try:
            round_to_inches = self.parse_measurement(round_to_str)
            if round_to_inches <= 0:
                return value
            return round(value / round_to_inches) * round_to_inches
        except:
            return value

def run_tests():
    """Import and run the comprehensive unit tests"""
    try:
        from test_calculator import run_tests_silent
        success, failure_count, total_count = run_tests_silent()
        
        if success:
            print(f"ALL {total_count} TESTS PASSED!")
            return True
        else:
            print(f"{failure_count} out of {total_count} tests FAILED!")
            return False
    except ImportError as e:
        print(f"Error importing test module: {e}")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False
