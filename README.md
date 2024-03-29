# FastAPI Simple Bills Management

This project is a simple and straightforward bills and invoicing management system. It supports adding and retrieving bills, with basic filtering support. It's built using FastAPI and PostgreSQL, uses Docker for deployment, and features authentication, logging, migrations system, etc.

### Requirements

This project supports Python versions greater than `3.11`.

- `fastapi`: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- `SQLAlchemy`: A SQL toolkit and ORM that provides a set of high-level API for connecting to relational databases.
- `pydantic`: A data validation and settings management library using Python type annotations.
- `asyncpg`: A library for accessing a PostgreSQL database from the asyncio framework.
- `fastapi-restful`: A library for building RESTful APIs with FastAPI.
- `passlib`: A password hashing library for Python that provides cross-platform implementations of over 30 password hashing algorithms.
- `pyjwt`: A Python library for encoding and decoding JSON Web Tokens (JWTs).
- `alembic`: A lightweight database migration tool for usage with SQLAlchemy.
- `python-dotenv`: A library for loading environment variables from a `.env` file.
- `pydantic-settings`: A library for managing application settings using Pydantic models.
- `aiosqlite`: A library for accessing a SQLite database from the asyncio framework.
- `pytz`: A library for working with time zones in Python.
- `starlette-context`: A library for managing context variables in Starlette and FastAPI applications.
- `uvicorn`: A lightning-fast ASGI server implementation, using uvloop and httptools.
- `typing-inspect`: A library for runtime inspection of Python typing information.
- `python-multipart`: A library for parsing multipart/form-data requests in Python.
- `argon2-cffi`: A Python binding of the Argon2 password hashing algorithm.

### Steps to Run the Project

1. Clone the project repository to your local machine using `git clone <repository-url>` command.
2. Navigate to the project directory using `cd <project-directory>` command.
3. Create a copy of the `sample.env` file. Adjust the credentials as per your needs and save the file as `.env` in the project root directory.
4. Build the image using Docker Compose `docker compose build`.
5. Start the services using Docker Compose `docker compose up`.

### Endpoint Details

This repository also includes the Postman Collection `postman_collection.json`. Please import it to Postman to test and trial the endpoints.

