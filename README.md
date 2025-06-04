# Feet & Inches Calculator

A Python-based calculator for performing mathematical operations on feet and inches measurements, with support for fractions and PEMDAS order of operations.

## Features

- **Measurement Input**: Supports various formats like:
  - `10' 11 1/2"` (feet and inches with fractions)
  - `5' 6"` (feet and inches)
  - `12"` (inches only)
  - `2'` (feet only)
  - `1 1/4"` (inches with fractions)

- **Mathematical Operations**: 
  - Addition (+)
  - Subtraction (-)
  - Multiplication (*, x, X)
  - Division (/, ÷)
  - Parentheses for order of operations

- **Rounding**: Round results to specified fractions (e.g., 1/8", 1/4", 1/2", 1")

- **History**: View calculation history with timestamps

- **Unit Testing**: Built-in tests to verify calculation accuracy

- **GUI Interface**: User-friendly interface built with FreeSimpleGUI

## Installation

1. **Install Python** (3.7 or higher)

2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```powershell
   python main.py
   ```

## Building Executable

To create a standalone executable file:

```powershell
python build.py
```

This will:
- Install all required dependencies
- Create a single executable file using PyInstaller
- Place the executable in the `dist` folder

## Usage Examples

### Basic Operations
- `10' + 2' 6"` → `12' 6"`
- `5' 6" - 1' 3"` → `4' 3"`
- `3' x 2` → `6'`
- `12" / 4` → `3"`

### With Fractions
- `10' 11 1/2" + 5' 10 1/8"` → `16' 9 5/8"`
- `1' 6 3/4" x 2` → `3' 1 1/2"`

### Order of Operations
- `(1' x 2 1/2") + 1"` → `2' 7"`
- `10' + (6" x 2)` → `11'`

### Rounding
Enter a rounding value like `1/8"`, `1/4"`, `1/2"`, or `1"` to round results to the nearest fraction.

## File Structure

```
calculator/
├── main.py                 # GUI application
├── calculator_engine.py    # Core calculation logic
├── build.py               # Build script for executable
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Dependencies

- **FreeSimpleGUI**: For the graphical user interface
- **PyInstaller**: For creating executable files
- **fractions**: For handling fraction arithmetic (built-in)

## Testing

Run the built-in unit tests by clicking the "Run Tests" button in the GUI, or run them directly:

```powershell
python calculator_engine.py
```

## Future Enhancements

- Support for metric units (mm, cm, m)
- More advanced mathematical functions
- Import/export calculation history
- Custom rounding increments

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Build Errors**: Ensure PyInstaller is properly installed:
   ```powershell
   pip install pyinstaller
   ```

3. **GUI Not Displaying**: Try updating FreeSimpleGUI:
   ```powershell
   pip install --upgrade FreeSimpleGUI
   ```

## License

This project is open source and available under the MIT License.
