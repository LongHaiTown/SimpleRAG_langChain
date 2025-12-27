@echo off
REM =====================================================
REM Quick Start Script for RAG Blog Chat System
REM =====================================================

echo.
echo ============================================================
echo   RAG Blog Chat System - Quick Start
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python first: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Checking dependencies...
pip show langchain >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
) else (
    echo [OK] Dependencies already installed
)

echo.
echo [2/4] Checking vector database...
if not exist "vectorstore\chroma.sqlite3" (
    echo [INFO] Vector database not found. Running embedding...
    echo This may take a few minutes...
    python embed_blog_posts.py
    if errorlevel 1 (
        echo [ERROR] Embedding failed!
        pause
        exit /b 1
    )
) else (
    echo [OK] Vector database exists
    echo [?] Do you want to re-embed blogs? (y/N)
    set /p re_embed=
    if /i "%re_embed%"=="y" (
        python embed_blog_posts.py
    )
)

echo.
echo [3/4] Running system tests...
python test_system.py
if errorlevel 1 (
    echo [WARNING] Some tests failed, but continuing...
)

echo.
echo [4/4] Starting API server...
echo.
echo ============================================================
echo   API Server is starting...
echo   URL: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo ============================================================
echo.
echo   Press Ctrl+C to stop the server
echo.

uvicorn api.app:app --reload --port 8000
