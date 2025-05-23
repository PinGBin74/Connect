# 🚀 Connect - Modern Social Platform API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)

</div>

## 🌟 Overview

Connect is a powerful, scalable, and modern social platform API built with FastAPI. It provides a robust foundation for building social networking applications with features like user management, content sharing, and real-time interactions.

## ✨ Key Features

- 🔐 **Secure Authentication System**
  - JWT-based authentication
  - Role-based access control
  - Secure password hashing

- 👥 **User Management**
  - User profiles
  - User settings
  - Subscription management
  - Social connections

- 📝 **Content Management**
  - Post creation and management
  - Rich media support
  - Content moderation

- 🔄 **Real-time Features**
  - Asynchronous processing with Celery
  - Background task management
  - Event-driven architecture

- 🛡️ **Security & Monitoring**
  - Sentry integration for error tracking
  - CORS middleware
  - Comprehensive logging
  - Rate limiting

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **Containerization**: Docker
- **Testing**: Pytest
- **Code Quality**: Ruff, Flake8

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Make (optional, for using Makefile commands)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/PinGBin74/connect.git
cd connect
```

2. Set up environment variables:
```bash
cp .local.env.example .local.env
```

3. Start the application:
```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### Development Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
poetry install 
```

3. Run the development server:
```bash
make run
```

## 🛠️ Available Make Commands

The project includes several useful make commands to simplify development:

```bash
make run              # Run the application with uvicorn (host: 127.0.0.1, port: 8080)
make start-celery-beat    # Start Celery beat scheduler
make start-celery-worker  # Start Celery worker
make install LIBRARY=<package>  # Install a new dependency
make uninstall LIBRARY=<package>  # Remove a dependency
make migrate-create MIGRATION="<message>"  # Create a new database migration
make migrate-apply  # Apply pending database migrations
make help          # Show all available commands
```

## 📚 API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

Run the test suite:
```bash
make test
```

## 🐳 Docker Support

The project includes Docker configuration for easy deployment:

- `Dockerfile` - Main application container
- `docker-compose.yml` - Development environment
- `docker-compose.test.yml` - Testing environment

## 📦 Project Structure

```
connect/
├── app/
│   ├── users/           # User management
│   ├── posts/           # Content management
│   ├── infrastructure/  # Core infrastructure
│   └── yandex_disk/     # File storage integration
├── tests/              # Test suite
├── docker-compose.yml  # Docker configuration
└── makefile           # Development commands
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👥 Authors

- Anton Fayfer

## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- All contributors who have helped shape this project

---
