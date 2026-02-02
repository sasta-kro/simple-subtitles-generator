#!/bin/bash

# This script checks for a Python virtual environment and creates it if it doesn't exist.
# It then installs the required dependencies and runs the main Python script.

# Checking if the venv directory exists.
if [ ! -d ".venv" ]; then
    echo "First time setup detected. Installing dependencies..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Running the main script.
echo "Starting the subtitle generation process..."
python3 main.py

# Deactivating the virtual environment.
deactivate
