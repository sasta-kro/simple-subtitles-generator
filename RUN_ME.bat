@echo off

REM # This script checks for a Python virtual environment and creates it if it doesn't exist.
REM # It then installs the required dependencies and runs the main Python script.

REM # Checking if the venv directory exists.
IF NOT EXIST .venv (
    echo "First time setup detected. Installing dependencies..."
    python -m venv .venv
    CALL .venv\Scripts\activate.bat
    pip install -r requirements.txt
) ELSE (
    CALL .venv\Scripts\activate.bat
)

REM # Running the main script.
echo "Starting the subtitle generation process..."
python main.py

REM # Pausing to keep the window open.
pause
