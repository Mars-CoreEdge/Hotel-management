@echo off
echo 🏨 Building Hotel Management System Docker Image...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Docker Compose not found. Trying docker compose...
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Docker Compose is not available. Please install Docker Compose.
        pause
        exit /b 1
    )
    set DOCKER_COMPOSE=docker compose
) else (
    set DOCKER_COMPOSE=docker-compose
)

echo ✅ Docker and Docker Compose are available

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚠️ .env file not found. Creating from template...
    copy env.template .env
    echo ⚠️ Please edit .env file with your configuration before deployment!
)

REM Build the Docker image
echo ✅ Building Docker image...
docker build -t hotel-management:latest .

if errorlevel 1 (
    echo ❌ Failed to build Docker image
    pause
    exit /b 1
)

echo ✅ Docker image built successfully!

REM Create data directory for database persistence
if not exist "data" mkdir data
echo ✅ Created data directory for database persistence

echo.
echo 🚀 Build completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Run: %DOCKER_COMPOSE% up -d
echo 3. Access your API at: http://localhost:8001
echo.
echo For production with nginx: %DOCKER_COMPOSE% --profile production up -d
echo.
pause 