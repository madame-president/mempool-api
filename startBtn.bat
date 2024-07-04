@echo off
:loop
python run.py
echo.
echo Press any key to run the program again or CTRL+C to exit...
pause >nul
goto loop