@echo off
echo ========================================
echo  GitHub Repository Setup Helper
echo ========================================
echo.

echo This script will help you set up Git for this project.
echo.
echo Prerequisites:
echo   - Git must be installed (download from git-scm.com)
echo   - You should have a GitHub account
echo.
pause

REM Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Git is not installed or not in PATH!
    echo.
    echo Please install Git from: https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

echo.
echo Git found! Proceeding...
echo.

REM Initialize repository if not already done
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo.
) else (
    echo Git repository already initialized.
    echo.
)

REM Set up .gitignore if not exists
if not exist ".gitignore" (
    echo ERROR: .gitignore not found!
    echo Please make sure .gitignore exists in the project root.
    pause
    exit /b 1
)

REM Add all files
echo Adding files to Git...
git add .
echo.

REM Check status
echo Current status:
git status
echo.

REM Prompt for commit
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Initial commit - Sailaway to Windy GPS Bridge

echo.
echo Committing with message: %COMMIT_MSG%
git commit -m "%COMMIT_MSG%"
echo.

echo ========================================
echo  Next Steps:
echo ========================================
echo.
echo 1. Create a repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Copy the repository URL (it will look like):
echo    https://github.com/YOUR_USERNAME/SA32windy.git
echo.
echo 3. Run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/SA32windy.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. GitHub Actions will automatically build the x64 executable!
echo.
echo See GITHUB_SETUP.md for detailed instructions.
echo.

pause
