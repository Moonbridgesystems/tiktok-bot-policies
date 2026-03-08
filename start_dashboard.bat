@echo off
echo ========================================
echo TikTok Viral Clothing Bot - DASHBOARD
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install requirements
echo Installing/updating requirements...
pip install -r requirements.txt
echo.

echo ========================================
echo Starting dashboard...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop
echo ========================================
echo.

REM Run the dashboard
python main.py --dashboard

pause
