"""
Build script for creating the executable using PyInstaller
"""

import subprocess
import sys
import os


def build_executable():
    """Build the executable using PyInstaller"""
    
    print("Building Feet & Inches Calculator executable...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Create a single executable file
        '--windowed',                   # Don't show console window
        '--name=FeetInchesCalculator',  # Name of the executable
        '--icon=calculator.ico',        # Icon file (optional)
        '--add-data=calculator_engine.py;.',  # Include the calculator engine
        'main.py'                       # Main script
    ]
    
    # Remove the icon parameter if icon file doesn't exist
    if not os.path.exists('calculator.ico'):
        cmd = [arg for arg in cmd if not arg.startswith('--icon')]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print("Executable created in 'dist' folder")
        
        # Display any warnings
        if result.stderr:
            print("\nWarnings:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print("Build failed!")
        print("Error:", e.stderr)
        return False
    
    return True


def install_dependencies():
    """Install required dependencies"""
    
    print("Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("Failed to install dependencies!")
        print("Error:", str(e))
        return False


if __name__ == "__main__":
    print("Feet & Inches Calculator Build Script")
    print("=" * 40)
    
    # Install dependencies first
    if not install_dependencies():
        sys.exit(1)
    
    # Build executable
    if not build_executable():
        sys.exit(1)
    
    print("\nBuild completed successfully!")
    print("You can find the executable in the 'dist' folder.")
