
# WittyWeather

A full-stack weather application that delivers real-time weather data with context-aware, humorous responses.

## Overview
WittyWeatherV2 is a full-stack web application that fetches real-time weather data from the OpenWeatherMap API
and presents it through a Flask-based REST API and a simple frontend interface.

The application includes user authentication, caching, database persistence, and is fully containerized
using Docker for consistent development and deployment.

## Tech Stack

**Client**
- HTML
- CSS
- JavaScript

**Server**
- Python
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Authlib (OAuth 2.0)
- Alembic

**Database & Cache**
- MySQL
- Redis

**Infrastructure**
- Docker
- Docker Compose
- Nginx
- Gunicorn


## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Setup

Clone the repository:

```bash
git clone https://github.com/simranjitdehal/wittyWeatherV2.git

cd wittyWeatherV2

```

Create a `.env` file inside the `backend/` directory and set the required environment variables listed below.

## The application requires the following environment variables:

### External Services
- OPENWEATHER_API_KEY – API key for OpenWeatherMap

### Authentication
- JWT_SECRET_KEY – Secret key for JWT authentication
- GOOGLE_CLIENT_ID – OAuth client ID for Google login
- GOOGLE_CLIENT_SECRET – OAuth client secret for Google login

### Database
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_DATABASE
- MYSQL_ROOT_PASSWORD
- SQLALCHEMY_DATABASE_URI

### Cache
- REDIS_HOST
- REDIS_PORT

## Start the application:

```bash
docker compose up --build
```
Once the containers are running, open the application in your browser:

- Frontend: http://localhost (or the port configured in `docker-compose.yml`)
- Backend API: http://localhost/api



## API Reference

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `POST /api/login/google` - Login using google OAuth

### Weather
- `GET /api/get_weather?city=${city}` - Fetch weather with contextual jokes (cached with Redis)


## License

[MIT](https://choosealicense.com/licenses/mit/)

Copyright (c) 2025 Simranjit