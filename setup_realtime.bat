@echo off
echo ========================================
echo Safe Real-Time Setup Guide
echo ========================================
echo.
echo This wizard will help you configure real-time TikTok data collection.
echo.
echo Available methods:
echo   1. Official TikTok API (safest, requires approval)
echo   2. Apify (easiest, cloud-based, paid)
echo   3. CSV Import (manual data entry, free)
echo   4. Demo Mode (for testing)
echo.
choice /C 1234 /N /M "Choose method (1-4): "

if errorlevel 4 goto demo
if errorlevel 3 goto csv
if errorlevel 2 goto apify
if errorlevel 1 goto official

:official
echo.
echo ========================================
echo Official TikTok API Setup
echo ========================================
echo.
echo Steps:
echo   1. Visit: https://developers.tiktok.com/
echo   2. Create an account and apply for API access
echo   3. Create an app to get your credentials
echo   4. Wait for approval (can take days/weeks)
echo.
echo After approval, you'll receive:
echo   - Client Key
echo   - Client Secret
echo.
pause
echo.
echo Creating .env file...
(
echo # TikTok Official API
echo TIKTOK_CLIENT_KEY=your_client_key_here
echo TIKTOK_CLIENT_SECRET=your_client_secret_here
echo.
echo # Data source
echo DATA_SOURCE=official
) > .env
echo.
echo ✓ .env file created
echo.
echo Next steps:
echo   1. Edit .env file and add your credentials
echo   2. Run: python main.py --mode once
echo.
pause
goto end

:apify
echo.
echo ========================================
echo Apify Setup (Recommended for beginners)
echo ========================================
echo.
echo Steps:
echo   1. Visit: https://apify.com
echo   2. Sign up (free trial available)
echo   3. Go to Settings → Integrations
echo   4. Copy your API token
echo.
start https://console.apify.com/account/integrations
pause
echo.
set /p APIFY_TOKEN="Enter your Apify API token: "
echo.
echo Creating .env file...
(
echo # Apify API
echo APIFY_API_TOKEN=%APIFY_TOKEN%
echo.
echo # Data source
echo DATA_SOURCE=apify
) > .env
echo.
echo ✓ .env file created with your token
echo.
echo Next steps:
echo   1. Run: python main.py --mode once
echo   2. Check your Apify dashboard for usage
echo.
echo Note: Apify charges per use. Free tier: $5 credit
echo.
pause
goto end

:csv
echo.
echo ========================================
echo CSV Import Setup
echo ========================================
echo.
echo This method lets you manually collect data and import it.
echo.
echo Steps:
echo   1. Manually browse TikTok
echo   2. Copy video data to CSV file
echo   3. Import into the bot
echo.
echo Creating .env file and CSV template...
(
echo # Data source
echo DATA_SOURCE=csv
) > .env

REM Create CSV template
if not exist "import_data" mkdir import_data
(
echo video_id,video_link,thumbnail_url,views,likes,total_comments,post_time,author,comments
echo 7123456789,https://www.tiktok.com/@user/video/7123456789,https://example.com/thumb.jpg,50000,3000,150,2026-03-07T12:00:00,fashionuser,Love this!^|Where can I buy?^|Amazing!
) > import_data\csv_template.csv

echo.
echo ✓ .env file created
echo ✓ CSV template created at: import_data\csv_template.csv
echo.
echo Next steps:
echo   1. Open import_data\csv_template.csv
echo   2. Add your TikTok video data
echo   3. Run: python main.py --mode once
echo.
pause
goto end

:demo
echo.
echo ========================================
echo Demo Mode Setup
echo ========================================
echo.
echo Demo mode uses sample data for testing.
echo No API credentials needed.
echo.
echo Creating .env file...
(
echo # Data source
echo DATA_SOURCE=demo
) > .env
echo.
echo ✓ .env file created
echo.
echo Next steps:
echo   1. Run: python main.py --mode once
echo   2. Check dashboard at http://localhost:5000
echo.
pause
goto end

:end
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the bot:
echo   python main.py --mode once
echo.
echo To start the dashboard:
echo   python main.py --dashboard
echo.
pause
