"""
Feet and Inches Calculator GUI
A simple calculator for feet and inches measurements with GUI interface
"""

import FreeSimpleGUI as sg
from calculator_engine import FeetInchesCalculator
import traceback
from datetime import datetime


class CalculatorGUI:
    """GUI wrapper for the feet and inches calculator"""
    
    def __init__(self):
        self.calculator = FeetInchesCalculator()
        self.history = []
        
        # Set theme
        sg.theme('LightBlue3')
        
        # Define layout
        self.layout = [
            [sg.Text('Feet & Inches Calculator', font=('Arial', 16, 'bold'), justification='center')],
            [sg.Text('')],
            
            # Main input section
            [sg.Text('Enter equation:', font=('Arial', 10))],
            [sg.InputText(key='-INPUT-', size=(60, 1), font=('Arial', 12), focus=True)],
            [sg.Button('Solve', bind_return_key=True, size=(10, 1)), 
             sg.Button('Clear Input', size=(10, 1))],
            
            [sg.Text('')],
            
            # Rounding section
            [sg.Text('Round to (optional):', font=('Arial', 10))],
            [sg.InputText(key='-ROUND-', size=(20, 1), font=('Arial', 12)),
             sg.Text('Example: 1/8", 1/4", 1/2", 1"', font=('Arial', 9), text_color='gray')],
            
            [sg.Text('')],
            
            # Result section
            [sg.Text('Result:', font=('Arial', 12, 'bold'))],
            [sg.Text('', key='-RESULT-', font=('Arial', 14, 'bold'), text_color='blue', size=(60, 2))],
            
            [sg.Text('')],
            
            # History section
            [sg.Text('History:', font=('Arial', 12, 'bold'))],
            [sg.Multiline('', key='-HISTORY-', size=(70, 10), font=('Arial', 10), 
                         disabled=True, autoscroll=True, horizontal_scroll=True)],
            [sg.Button('Clear History', size=(12, 1))],
            [sg.Text('')],
            [sg.Button('Exit', size=(10, 1))]
        ]
        
        # Create window
        self.window = sg.Window('Feet & Inches Calculator', self.layout, 
                               resizable=True, finalize=True, 
                               icon=None, size=(600, 700))
        
        # Set focus to input field
        self.window['-INPUT-'].set_focus()
    
    def add_to_history(self, equation: str, result: str, rounded_to: str = None):
        """Add calculation to history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if rounded_to:
            history_entry = f"[{timestamp}] {equation} = {result} (rounded to {rounded_to})\n"
        else:
            history_entry = f"[{timestamp}] {equation} = {result}\n"
        
        self.history.append(history_entry)
        
        # Update history display
        history_text = ''.join(self.history)
        self.window['-HISTORY-'].update(history_text)
    
    def solve_equation(self, equation: str, round_to: str = None):
        """Solve the equation and update the result"""
        try:
            if not equation.strip():
                self.window['-RESULT-'].update("Please enter an equation")
                return
            
            # Evaluate the expression
            result_inches = self.calculator.evaluate_expression(equation)
            
            # Format the result
            if round_to and round_to.strip():
                formatted_result = self.calculator.format_result(result_inches, round_to.strip())
                self.add_to_history(equation, formatted_result, round_to.strip())
            else:
                formatted_result = self.calculator.format_result(result_inches)
                self.add_to_history(equation, formatted_result)
            
            # Update result display
            self.window['-RESULT-'].update(formatted_result)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.window['-RESULT-'].update(error_msg)
            self.add_to_history(equation, error_msg)
    
    def clear_history(self):
        """Clear the calculation history"""
        self.history = []
        self.window['-HISTORY-'].update('')
    
    def run(self):
        """Main event loop"""
        while True:
            event, values = self.window.read()
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            
            elif event == 'Solve':
                equation = values['-INPUT-']
                round_to = values['-ROUND-']
                self.solve_equation(equation, round_to)
            
            elif event == 'Clear Input':
                self.window['-INPUT-'].update('')
                self.window['-RESULT-'].update('')
                self.window['-INPUT-'].set_focus()
            
            elif event == 'Clear History':
                self.clear_history()
        
        self.window.close()


def main():
    """Main function to run the calculator GUI"""
    try:
        app = CalculatorGUI()
        app.run()
    except Exception as e:
        sg.popup_error(f"An error occurred: {str(e)}\n\n{traceback.format_exc()}")


if __name__ == "__main__":
    main()
