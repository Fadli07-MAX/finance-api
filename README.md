# Finance API
A production-ready REST API built with FastAPI, PostgreSQL, and SQLAlchemy. This project demonstrates modern backend development practices including JWT authentication, role-based access control, database migrations, automated testing, and Dockerized deployment.

# Overview
Finance API was developed as a portfolio project to showcase practical backend engineering skills using Python. The application provides user authentication, authorization, and CRUD operations through a well-structured and documented REST API.
The project follows industry-standard practices:
- Modular application structure
- Database schema migrations with Alembic
- Token-based authentication using JWT
- Role-based authorization (`user` and `admin`)
- Automated testing with Pytest
- Containerized development with Docker
- Source control with Git and GitHub

# Features
 Authentication and Authorization
- User registration
- Secure password hashing with bcrypt
- JWT-based login
- Protected endpoints
- Role-based access control

# Item Management
- Create items
- Retrieve item list
- Retrieve item by ID
- Delete items

# Database Management
- PostgreSQL integration
- SQLAlchemy ORM
- Alembic migrations

# Development Tooling
- Swagger/OpenAPI documentation
- Unit and integration tests
- Docker and Docker Compose

## Technology Stack
| Category         | Technology             |
| ---------------- | ---------------------- |
| Language         | Python 3.14            |
| Web Framework    | FastAPI                |
| ORM              | SQLAlchemy 2.0         |
| Database         | PostgreSQL             |
| Migrations       | Alembic                |
| Authentication   | Python-JOSE, Passlib   |
| Testing          | Pytest                 |
| Containerization | Docker, Docker Compose |
| Version Control  | Git, GitHub            |

# Project Structure
```text
finance-api/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── items.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── alembic/
│   └── versions/
├── tests/
│   └── test_main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
└── README.md
```

# Getting Started
 Prerequisites
Ensure the following software is installed:
- Python 3.14+
- PostgreSQL
- Docker Desktop (optional)
- Git

# Local Development Setup
 1. Clone the Repository
```bash
git clone https://github.com/Fadli07-MAX/finance-api.git
cd finance-api
```
 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
```
Windows PowerShell
```powershell
venv\Scripts\Activate.ps1
```
Windows Command Prompt
```cmd
venv\Scripts\activate
```
 3. Install Dependencies
```bash
pip install -r requirements.txt
```
 4. Run Database Migrations
```bash
alembic upgrade head
```
 5. Start the Development Server
```bash
uvicorn app.main:app --reload
```
 6. Access API Documentation
Open:
```text
http://127.0.0.1:8000/docs
```

# Running with Docker
Start the application and PostgreSQL database:
```bash
docker compose up --build
```
Stop the containers:
```bash
docker compose down
```
Swagger documentation:
```text
http://127.0.0.1:8000/docs
```

# Running Tests
```bash
python -m pytest -v
```

# Authentication Workflow
1. Register a new user via `POST /register`
2. Log in via `POST /login`
3. Copy the returned access token
4. Click **Authorize** in Swagger UI
5. Paste the token
6. Access protected endpoints such as `GET /me`


## Role-Based Access Control

| Role  | Permissions                     |
| ----- | ------------------------------- |
| user  | Access standard user endpoints  |
| admin | Access administrative endpoints |

Administrative endpoint example:

```http
GET /admin/users
```

# API Endpoints

| Method | Endpoint           | Description                     |
| -----: | ------------------ | ------------------------------- |
|   POST | `/register`        | Register a new user             |
|   POST | `/login`           | Obtain JWT access token         |
|    GET | `/me`              | Retrieve current user profile   |
|    GET | `/items`           | Retrieve all items              |
|   POST | `/items`           | Create a new item               |
|    GET | `/items/{item_id}` | Retrieve a specific item        |
| DELETE | `/items/{item_id}` | Delete an item                  |
|    GET | `/admin/users`     | Retrieve all users (admin only) |

# Deployment
This project is ready to be deployed to platforms such as:
- Railway
- Render
- DigitalOcean
- AWS

# Future Enhancements
 Planned improvements include:
- Refresh tokens
- Password reset functionality
- Pagination and filtering
- Structured logging
- Rate limiting
- CI/CD with GitHub Actions
- Monitoring and health checks

# Repository
GitHub Repository:
[https://github.com/Fadli07-MAX/finance-api](https://github.com/Fadli07-MAX/finance-api)

# Author
**Adi Candra Fadli**
Backend Developer focused on Python, FastAPI, machine learning, and systems engineering.
GitHub: [https://github.com/Fadli07-MAX](https://github.com/Fadli07-MAX)

# License
This project is available for educational and portfolio purposes.
