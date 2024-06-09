# FastAPI Template Project with Session Authentication, Jinja2, and HTMX

This project serves as a template for creating web applications using FastAPI, Jinja2 templates, and HTMX for dynamic interactions. The goal is to provide a ready-to-use framework that includes session-based authentication, admin interface with authentication, unit tests for CRUD operations and main routes, and Docker support. This allows developers to focus on implementing their specific logic without worrying about the underlying infrastructure and services.

## Features
- Session-based authentication
- SQLAlchemy admin with authentication
- Unit tests for CRUD operations and main routes
- Dockerfile for containerization

## Environment Variables
- `SECRET_KEY`: A secret key for securing the session data.
- `DB_URL`: The database URL in a format understood by SQLAlchemy. For example, `postgres://user:password@localhost/dbname`. More details can be found [here](https://pypi.org/project/dj-database-url/).
- `DEV`: Specifies the environment. Possible values are `Dev`, `Test`, `Prod`, or any other custom environment you might add.

## Running Tests
All tests use SQLite for the database (it is created locally). To run the unit tests for CRUD operations and main routes, use the following command:
```shell
make tests
```

## Usage

### In the local machine
You can start application by command:
```shell
make runserver
```

### Using docker
```shell
docker build -t fastapi-app:latest .
docker run -d -p 8000:5000 fastapi-app
```