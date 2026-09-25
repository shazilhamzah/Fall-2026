@echo off
title OWASP Juice Shop - IS Assignment 1
echo ============================================================
echo Starting OWASP Juice Shop on http://localhost:3000
echo Leave this terminal open while working on your assignment!
echo ============================================================
echo.
cd /d "%~dp0juice-shop"
npm start
pause

