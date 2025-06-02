@echo off
echo 🔍 Checking for required tools...

where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed. Install it here: https://www.python.org/downloads/
    exit /b 1
) ELSE (
    echo ✅ Python found
)

python -m pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ pip not found. You may need to reinstall Python or run: curl https://bootstrap.pypa.io/get-pip.py | python
    exit /b 1
) ELSE (
    echo ✅ pip found
)

python -m venv --help >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ venv module not available. You may need to reinstall Python with all options enabled.
    exit /b 1
) ELSE (
    echo ✅ venv module available
)

IF NOT EXIST requirements.txt (
    echo ❌ requirements.txt not found
    exit /b 1
) ELSE (
    echo ✅ requirements.txt found
)

IF NOT EXIST scrape_events.py (
    echo ❌ scrape_events.py not found
    exit /b 1
) ELSE (
    echo ✅ Scraper script found
)

IF NOT EXIST credentials.json (
    echo ❌ credentials.json not found
    exit /b 1
) ELSE (
    echo ✅ Google credentials file found
)

echo Creating virtual environment (if not exists)...
IF NOT EXIST env (
    python -m venv env
)

echo Activating virtual environment...
call env\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Running the scraper...
python scrape_events.py

IF %ERRORLEVEL% EQU 0 (
    echo ✅ Scraper completed successfully!
) ELSE (
    echo ❌ Scraper failed. Check for errors above.
)
echo ✅ Scraper finished at %TIME%
