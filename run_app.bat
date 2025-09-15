@echo off
echo Starting Word Frequency Analysis App...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo Installing requirements...
pip install -r requirements.txt

REM Check if Ollama is running
echo Checking Ollama connection...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo Warning: Ollama is not running or not accessible
    echo Please start Ollama with: ollama serve
    echo.
    echo You can still use the app for document analysis without AI chat
    echo.
)

REM Start the Streamlit app
echo Starting Streamlit app...
echo.
echo The app will open in your default browser at http://localhost:8501
echo Press Ctrl+C to stop the app
echo.
streamlit run app.py

pause
