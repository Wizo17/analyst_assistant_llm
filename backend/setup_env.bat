@echo off
echo Creating the virtual environment for api.
python -m venv venv

echo Environment activation
call venv\Scripts\activate

echo Installing dependencies.
pip install -r requirements.txt

echo Copying .env.
cp .env_example .env

echo Environment successfully configured!
pause