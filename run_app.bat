cd /d "%~dp0"
python main.py
timeout /t 2
start http://127.0.0.1:8000