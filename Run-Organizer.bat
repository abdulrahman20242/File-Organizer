@echo off
REM ==============================
REM File Organizer GUI Launcher
REM ==============================

REM تأكد إن الباتش شغال من نفس مكان الكود
cd /d "%~dp0"

REM تشغيل البرنامج باستخدام بايثون
python File-Organizer-GUI.py

pause
