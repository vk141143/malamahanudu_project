@echo off
echo Step 1: Committing changes locally...
git add .
git commit -m "Fix CORS and 500 errors: add blood_group column, fix validation, add global exception handler"

echo.
echo Step 2: Pushing to repository...
git push

echo.
echo Step 3: Copy these commands to run on your server:
echo ========================================
echo cd /path/to/your/project
echo git pull
echo python add_blood_group_to_applications.py
echo sudo systemctl restart your-service-name
echo ========================================
echo.
pause
