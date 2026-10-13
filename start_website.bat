@echo off
setlocal
cd /d "%~dp0"

set "URL=http://127.0.0.1:5000"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3 and make sure it is added to PATH.
    pause
    exit /b 1
)

curl.exe --silent --fail "%URL%" >nul 2>nul
if not errorlevel 1 (
    echo The website is already running. Opening it in your browser...
    start "" "%URL%"
    exit /b 0
)

python -c "import flask" >nul 2>nul
if errorlevel 1 (
    echo Installing the website dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Dependency installation failed. Check your Python and internet connection.
        pause
        exit /b 1
    )
)

echo Starting StayEase. This window will stay open while the website is running.
start "StayEase Website" /min "%ComSpec%" /k "cd /d ""%~dp0"" && python app.py"

for /l %%i in (1,1,30) do (
    curl.exe --silent --fail "%URL%" >nul 2>nul
    if not errorlevel 1 (
        echo Website is ready. Opening it in your browser...
        start "" "%URL%"
        exit /b 0
    )
    ping.exe -n 2 127.0.0.1 >nul
)

echo The website did not start. Check the minimized StayEase Website window for errors.
pause
exit /b 1
