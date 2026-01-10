@echo off
echo ========================================
echo Starting FastAPI Server
echo ========================================

REM Kill any existing processes on port 8000
echo Checking for existing processes on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo Starting server on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

REM Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause