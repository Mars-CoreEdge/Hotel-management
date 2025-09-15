# Hotel Management System

A comprehensive hotel management system with a React frontend and FastAPI backend.

## Project Structure

```
├── frontend/          # React frontend application
│   ├── src/          # Source code
│   ├── public/       # Static assets
│   ├── build/        # Production build
│   ├── package.json  # Dependencies
│   └── README.md     # Frontend documentation
│
├── backend/          # FastAPI backend application
│   ├── app/          # Main application code
│   ├── tests/        # Test files
│   ├── hotel.db      # SQLite database
│   ├── main.py       # Application entry point
│   ├── requirements.txt
│   ├── Dockerfile    # Docker configuration
│   ├── docker-compose.yml
│   ├── nginx.conf    # Nginx configuration
│   ├── build.bat     # Windows build script
│   └── build.sh      # Linux/Mac build script
│
├── docs/             # Documentation
├── env.template      # Environment variables template
├── supabase_bookings_schema.sql
└── SUPABASE_*.md     # Setup guides
```

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create environment file:
   ```bash
   copy ..\env.template .env
   # Edit .env with your configuration
   ```

4. Run the backend:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   copy ..\env.template .env
   # Edit .env with your configuration
   ```

4. Run the frontend:
   ```bash
   npm start
   ```

### Docker Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Build and run with Docker:
   ```bash
   # Windows
   build.bat
   docker-compose up -d
   
   # Linux/Mac
   chmod +x build.sh
   ./build.sh
   docker-compose up -d
   ```

## Features

- **Frontend**: React-based user interface with authentication
- **Backend**: FastAPI REST API with SQLite database
- **Authentication**: User registration, login, and role-based access
- **Room Management**: Create, update, and manage hotel rooms
- **Booking System**: Handle room bookings and reservations
- **Guest Management**: Manage guest information and profiles
- **AI Integration**: OpenAI-powered chatbot for customer service
- **Email Notifications**: Automated booking confirmations
- **Docker Support**: Containerized deployment

## Documentation

- [Complete Project Guide](docs/COMPLETE_PROJECT_GUIDE.md)
- [Quick Start Guide](docs/QUICK_START_GUIDE.md)
- [Authentication Setup](docs/AUTHENTICATION_SETUP.md)
- [Email Setup Guide](docs/EMAIL_SETUP_GUIDE.md)
- [API Key Setup](docs/API_KEY_SETUP.md)
- [Admin Setup Guide](docs/ADMIN_SETUP_GUIDE.md)
- [Docker Deployment](DOCKER_DEPLOYMENT.md)

## API Endpoints

- **Authentication**: `/auth/*`
- **Profile Management**: `/profile/*`
- **Room Management**: `/rooms/*`
- **Guest Management**: `/guests/*`
- **Booking Management**: `/bookings/*`
- **Customer Operations**: `/customer/*`
- **AI Chatbot**: `/ai/*`

## Environment Variables

See `env.template` for required environment variables.

## License

This project is licensed under the MIT License.