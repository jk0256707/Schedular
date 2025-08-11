# Django Scheduler System

This project is a scalable, dockerized scheduler system built with Django, Celery, PostgreSQL, and Redis.

## Features
- Task scheduling and execution
- Configurable schedules and task types
- Scalable with Celery workers
- Dockerized for easy deployment

## Getting Started

### Prerequisites
- Docker & Docker Compose

### Setup
1. Build and start all services:
   ```sh
   docker-compose up --build
   ```
2. Access Django at http://localhost:8000
3. Default DB credentials are in `docker-compose.yml`.

### Development
- Code lives in the `/code` directory (mounted in Docker).
- Use Django admin for managing tasks/configs.

## Services
- **web**: Django app
- **db**: PostgreSQL
- **redis**: Redis (Celery broker)
- **celery**: Celery worker
- **celery-beat**: Celery scheduler

## Environment Variables
See `docker-compose.yml` for all environment variables.

## License
MIT
