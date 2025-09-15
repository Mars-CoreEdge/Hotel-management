# 🏨 Hotel Management System - Docker Deployment Guide

This guide will help you deploy the Hotel Management System using Docker for production or development environments.

## 📋 Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **System Requirements**: 
  - RAM: 512MB minimum, 1GB recommended
  - Storage: 2GB available space
  - CPU: 1 core minimum

## 🚀 Quick Start

### 1. Build and Deploy (Simple)

**For Windows:**
```bash
# Run the build script
./build.bat

# Start the service
docker-compose up -d
```

**For Linux/Mac:**
```bash
# Make script executable
chmod +x build.sh

# Run the build script
./build.sh

# Start the service
docker-compose up -d
```

### 2. Manual Build (Alternative)

```bash
# Build the Docker image
docker build -t hotel-management:latest .

# Create environment file
cp env.template .env
# Edit .env with your configuration

# Start with Docker Compose
docker-compose up -d
```

## ⚙️ Configuration

### Environment Variables

Copy `env.template` to `.env` and configure:

```bash
# Required Configuration
EMAIL_ADDRESS=your-hotel-email@gmail.com
EMAIL_PASSWORD=your-app-password
HOTEL_NAME=Your Hotel Name
OPENAI_API_KEY=your-openai-key-here  # Optional for AI features
```

### Important Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8001` |
| `EMAIL_ADDRESS` | Hotel email for notifications | Required |
| `EMAIL_PASSWORD` | App password for email | Required |
| `HOTEL_NAME` | Your hotel name | `Grand Hotel` |
| `OPENAI_API_KEY` | For AI reception features | Optional |
| `DEBUG` | Debug mode | `False` |

## 🏗️ Deployment Options

### 1. Development Deployment

```bash
# Start in development mode
docker-compose up

# View logs
docker-compose logs -f
```

### 2. Production Deployment

```bash
# Start with nginx reverse proxy
docker-compose --profile production up -d

# Access via:
# - API: http://localhost:8001
# - Through nginx: http://localhost:80
```

### 3. Custom Port Deployment

```bash
# Edit docker-compose.yml ports section:
ports:
  - "8080:8001"  # Change 8080 to your desired port

# Then start
docker-compose up -d
```

## 📁 File Structure

```
hotel-management/
├── Dockerfile              # Main application container
├── docker-compose.yml      # Service orchestration
├── nginx.conf              # Nginx configuration
├── .dockerignore           # Files to exclude from build
├── env.template            # Environment template
├── build.sh                # Linux/Mac build script
├── build.bat               # Windows build script
├── data/                   # Database persistence (auto-created)
└── app/                    # Application code
```

## 🔧 Advanced Configuration

### SSL/HTTPS Setup

1. Uncomment SSL section in `nginx.conf`
2. Place certificates in `./ssl/` directory:
   ```
   ssl/
   ├── cert.pem
   └── key.pem
   ```
3. Deploy with production profile:
   ```bash
   docker-compose --profile production up -d
   ```

### Database Persistence

Database data is automatically persisted in the `data/` directory via Docker volumes.

### Email Configuration

For Gmail:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in `EMAIL_PASSWORD`

## 📊 Monitoring & Management

### Health Checks

```bash
# Check container health
docker-compose ps

# Check API health
curl http://localhost:8001/health
```

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs hotel-api

# Follow logs
docker-compose logs -f
```

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Check what's using the port
netstat -tlnp | grep :8001

# Change port in docker-compose.yml
ports:
  - "8002:8001"  # Use 8002 instead
```

**Database Issues:**
```bash
# Reset database
docker-compose down
rm -rf data/
docker-compose up -d
```

**Email Not Working:**
- Verify Gmail App Password
- Check firewall settings
- Ensure `EMAIL_DEMO_MODE=False` for real emails

**Build Failures:**
```bash
# Clean build
docker system prune -a
docker-compose build --no-cache
```

### Log Analysis

```bash
# Container logs
docker logs hotel-management-api

# Database logs
docker-compose exec hotel-api ls -la data/

# Nginx logs (if using production profile)
docker logs hotel-nginx
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` file
2. **API Keys**: Use environment variables only
3. **Firewall**: Restrict access to necessary ports
4. **SSL**: Enable HTTPS for production
5. **Updates**: Keep Docker images updated

## 📈 Performance Tuning

### Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  hotel-api:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

### Scaling

```bash
# Scale API service
docker-compose up -d --scale hotel-api=3

# With load balancer
docker-compose --profile production up -d --scale hotel-api=3
```

## 🌐 Cloud Deployment

### AWS ECS
```bash
# Build for ARM64 (if using ARM instances)
docker build --platform linux/arm64 -t hotel-management:latest .
```

### Google Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/hotel-management
```

### DigitalOcean Apps
```bash
# Use docker-compose.yml directly in Apps Platform
```

## 🎯 API Endpoints

Once deployed, access these endpoints:

- **API Documentation**: `http://localhost:8001/docs`
- **Health Check**: `http://localhost:8001/health`
- **Room Management**: `http://localhost:8001/rooms`
- **Booking System**: `http://localhost:8001/bookings`
- **AI Reception**: `http://localhost:8001/ai/chat`

## 📞 Support

For deployment issues:
1. Check the logs: `docker-compose logs`
2. Verify configuration: `cat .env`
3. Test connectivity: `curl http://localhost:8001/health`
4. Review this guide's troubleshooting section

---

**🏨 Happy Hosting! Your Hotel Management System is ready for deployment.** 