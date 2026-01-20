@echo off
echo Deploying fixes...
echo.

git add .
git commit -m "Fix CORS and 500 errors: add blood_group column, fix validation, add global exception handler"
git push

echo.
echo Deployment complete!
echo.
echo If you're using a service like Render/Heroku, it will auto-deploy.
echo Otherwise, SSH to your server and run: git pull
pause
