#!/bin/bash

echo "Starting Word Frequency Analysis App..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.11+ and try again"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Check if Ollama is running
echo "Checking Ollama connection..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Warning: Ollama is not running or not accessible"
    echo "Please start Ollama with: ollama serve"
    echo
    echo "You can still use the app for document analysis without AI chat"
    echo
fi

# Start the Streamlit app
echo "Starting Streamlit app..."
echo
echo "The app will open in your default browser at http://localhost:8501"
echo "Press Ctrl+C to stop the app"
echo
streamlit run app.py
