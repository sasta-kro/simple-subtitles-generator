@echo off
setlocal

REM --- CONFIGURATION ---
set "RUNTIME=python_runtime_windows\python.exe"
set "PIP=python_runtime_windows\Scripts\pip.exe"
REM ---------------------

echo ===================================================
echo   Subtitle Generator (Self-Contained)
echo ===================================================

REM 1. Check if we have PIP installed in our local runtime
IF NOT EXIST "%PIP%" (
    echo [INFO] Installing Pip for local Python...

    REM Download get-pip.py to a temp file
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

    REM Install pip using our local python
    "%RUNTIME%" get-pip.py --no-warn-script-location

    REM Delete the installer
    del get-pip.py
)

REM 2. Install Dependencies (Using our local pip)
echo [INFO] Checking dependencies...
"%RUNTIME%" -m pip install -r requirements.txt --no-warn-script-location

REM 3. Set the PYTHONPATH to the current directory to ensure 'src' is found.
set "PYTHONPATH=%CD%"

REM 4. Run the App
echo [INFO] Starting the generator...
"%RUNTIME%" main.py

echo.
echo ===================================================
echo   Process Finished.
echo ===================================================
pause
