@echo off
title Push Mekuria to GitHub
cd /d "%~dp0"
echo ========================================================
echo  Pushing Mekuria AI Assistant to GitHub...
echo  Repository: https://github.com/programmersam000-svg/Mekuria-SI-Assistant.git
echo ========================================================
echo.
git push -u origin main
echo.
echo Pushing complete! Press any key to exit.
pause
