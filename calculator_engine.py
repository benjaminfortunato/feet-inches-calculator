import re
from fractions import Fraction

class FeetInchesCalculator:
    def __init__(self):
        pass

    def parse_measurement(self, text: str) -> float:
        """Parse a measurement string and return total inches as float"""
        text = text.strip()
        
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
        feet = int(total_inches // 12)
        remaining_inches = total_inches % 12
        
        if remaining_inches == 0:
            if feet == 0:
                return '0"'
            return f"{feet}'"
        
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
        
        return ' '.join(result_parts) if result_parts else '0"'

    def evaluate_expression(self, expression: str) -> float:
        """Evaluate a mathematical expression with feet and inches measurements"""
        expression = expression.strip()
        
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
            raise ValueError(f"Error evaluating expression: {str(e)}")

    def _extract_measurements(self, expression: str) -> dict:
        """Extract all measurements from expression and convert to inches"""
        measurements = {}
        
        # Process from most specific to least specific to avoid partial matches
        temp_expression = expression
        
        # First pass: feet with fractions
        matches = re.findall(r"\d+'\s*\d+/\d+\"", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Second pass: feet with inches
        matches = re.findall(r"\d+'\s*\d+\"", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Third pass: feet only
        matches = re.findall(r"\d+'(?=\s|$|[+\-*/()])", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Fourth pass: pure fractions with quotes
        matches = re.findall(r"\d+/\d+\"", temp_expression)
        for match in matches:
            measurements[match] = self.parse_measurement(match)
            temp_expression = temp_expression.replace(match, " PLACEHOLDER ")
        
        # Fifth pass: inches only
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
