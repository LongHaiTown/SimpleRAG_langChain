@echo off
echo ============================================================
echo Starting RAG Blog Chat API Server
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/2] Checking vector database...
if not exist "vectorstore" (
    echo Warning: Vector database not found!
    echo Please run: python embed_blog_posts.py
    pause
    exit /b 1
)

echo [2/2] Starting API server...
echo API will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn api.app:app --reload --port 8000
