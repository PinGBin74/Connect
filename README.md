# 🚀 Connect - Modern Social Platform API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Yandex.Disk](https://img.shields.io/badge/Yandex.Disk-FF0000?style=for-the-badge&logo=yandex&logoColor=white)

</div>

## 🌟 Overview | Обзор

Connect - это мощный, масштабируемый и современный API социальной платформы, построенный на FastAPI. Он предоставляет надежную основу для создания социальных сетей с функциями управления пользователями, обмена контентом и взаимодействия в реальном времени.

## ✨ Key Features | Основные возможности

- 🔐 **Secure Authentication System | Система безопасной аутентификации**
  - JWT-based authentication | Аутентификация на основе JWT
  - Role-based access control | Контроль доступа на основе ролей
  - Secure password hashing | Безопасное хеширование паролей

- 👥 **User Management | Управление пользователями**
  - User profiles | Профили пользователей
  - User settings | Настройки пользователей
  - Subscription management | Управление подписками
  - Social connections | Социальные связи

- 📝 **Content Management | Управление контентом**
  - Post creation and management | Создание и управление постами
  - Rich media support | Поддержка медиафайлов
  - Content moderation | Модерация контента

- 🔄 **Real-time Features | Функции реального времени**
  - Asynchronous processing with Celery | Асинхронная обработка с Celery
  - Background task management | Управление фоновыми задачами
  - Event-driven architecture | Событийно-ориентированная архитектура

- 🛡️ **Security & Monitoring | Безопасность и мониторинг**
  - Sentry integration for error tracking | Интеграция Sentry для отслеживания ошибок
  - CORS middleware | CORS middleware
  - Comprehensive logging | Комплексное логирование
  - Rate limiting | Ограничение частоты запросов

- 💾 **Yandex.Disk Integration | Интеграция с Яндекс.Диском**
  - File storage and management | Хранение и управление файлами
  - Automatic file synchronization | Автоматическая синхронизация файлов
  - Secure file sharing | Безопасный обмен файлами

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

The API will be available at `http://localhost:8080`

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
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

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

## 📦 Project Structure | Структура проекта

```
connect/
├── app/
│   ├── users/                    # User management | Управление пользователями
│   │   ├── auth/                # Authentication | Аутентификация
│   │   ├── user_profile/        # User profiles | Профили пользователей
│   │   ├── subscription/        # Subscription management | Управление подписками
│   │   └── users_settings/      # User settings | Настройки пользователей
│   │
│   ├── posts/                   # Content management | Управление контентом
│   │   ├── handlers/           # API endpoints | API эндпоинты
│   │   ├── models/             # Database models | Модели базы данных
│   │   └── services/           # Business logic | Бизнес-логика
│   │
│   ├── infrastructure/          # Core infrastructure | Основная инфраструктура
│   │   ├── celery/             # Celery configuration | Конфигурация Celery
│   │   ├── database/           # Database setup | Настройка базы данных
│   │   └── redis/              # Redis configuration | Конфигурация Redis
│   │
│   ├── yandex_disk/            # Yandex.Disk integration | Интеграция с Яндекс.Диском
│   │   ├── handlers/           # API endpoints | API эндпоинты
│   │   ├── models/             # Data models | Модели данных
│   │   └── services/           # Yandex.Disk API integration | Интеграция с API Яндекс.Диска
│   │
│   ├── main.py                 # Application entry point | Точка входа приложения
│   ├── settings.py             # Application settings | Настройки приложения
│   └── dependecy.py            # Dependency injection | Внедрение зависимостей
│
├── tests/                      # Test suite | Набор тестов
├── docker-compose.yml          # Docker configuration | Конфигурация Docker
└── makefile                    # Development commands | Команды разработки
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
