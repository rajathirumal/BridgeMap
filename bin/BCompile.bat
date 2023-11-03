@echo off

set "PARENT=bridge"

REM Check if the current directory ends with '\bin'
cd
if "%CD:~-4%" == "\bin" (
    cd ..
)

REM Execute Python script with arguments
python3.11 "%PARENT%\main.py" BCompile %*
