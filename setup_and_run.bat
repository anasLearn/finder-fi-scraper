@echo off

REM Check if the virtual environment directory exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
echo Activating virtual environment...
call .\venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Run the main Python script
echo Running main.py...
python main.py

REM Keep the window open after execution
pause
