@echo off
echo ========================================
echo TikTok Viral Clothing Bot - START
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

REM Ensure playwright is installed
echo Checking Playwright installation...
playwright install
echo.

echo ========================================
echo Starting bot in continuous mode...
echo Press Ctrl+C to stop
echo ========================================
echo.

REM Run the bot
python main.py --mode continuous

pause
