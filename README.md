# FastAPI-01: Social Media Backend API

## Project Overview

This is a backend API project built with FastAPI in Python, implementing a simple social media-like application. It supports user authentication, post management, and voting on posts. The project uses PostgreSQL as the database and includes features for secure authentication via JWT tokens.

## Features

### User Management

- User registration (POST `/users`): Create a new user with email, password, and optional phone number.
- User retrieval (GET `/users/{id}`): Fetch details of a specific user by ID.

### Authentication

- Login (POST `/login`): Authenticate with email and password to receive a JWT access token.
- JWT-based authorization for protected endpoints.

### Post Management

- Create post (POST `/posts`): Add a new post with title, content, and published status (requires authentication; owner is set to the current user).
- Retrieve all posts (GET `/posts`): List posts with pagination (limit and skip), search by title, and include vote counts. Optionally filter to show only the current user's posts.
- Retrieve single post (GET `/posts/{id}`): Get details of a specific post including vote count.
- Update post (PUT `/posts/{id}`): Edit a post (only by the owner).
- Delete post (DELETE `/posts/{id}`): Remove a post (only by the owner).

### Voting System

- Vote on post (POST `/votes`): Upvote (dir=1) or remove vote/downvote (dir=0) on a post. Prevents duplicate votes and checks for post existence.

### Other

- Root endpoint (GET `/`): Returns a simple "Hello World" message.
- CORS support for specified origins (e.g., https://www.google.com).
- Ownership enforcement: Users can only modify or delete their own posts.
- Timestamps: Automatic created_at fields for users, posts, and votes.

## Libraries and Dependencies

The project dependencies are listed in `requirements.txt`. Here's a breakdown with their purposes:

- **fastapi**: The core web framework for building the API with automatic interactive documentation (Swagger UI) and async support.
- **sqlalchemy**: ORM (Object-Relational Mapping) library for database interactions, defining models, and handling queries in an object-oriented way.
- **psycopg2**: PostgreSQL database adapter for Python, enabling connection to the Postgres database.
- **passlib**: Password hashing library (using bcrypt) for securely storing and verifying user passwords.
- **python-jose**: Library for handling JWT (JSON Web Tokens) encoding and decoding for authentication.
- **pydantic-settings**: Extension of Pydantic for managing application settings and configurations from environment variables or files.
- **alembic**: Database migration tool for version control of schema changes, allowing creation and management of tables based on models.
- **python-multipart**: Handles form data parsing, useful for file uploads or multipart requests (though not heavily used here).
- **uvicorn**: ASGI server for running the FastAPI application in development or production.

## Important Aspects

### Database Setup

- Uses PostgreSQL database named `fastapi-01`.
- Tables are defined via SQLAlchemy models and can be created/migrated using Alembic (`alembic upgrade head`).

### Configuration

- Settings like database URL, secret key for JWT, and token expiration are loaded from a `.env` file via `pydantic-settings`.

### Project Structure

- `app/`: Core application code.
  - `main.py`: Entry point, app initialization.
  - `config.py`: Configuration loading.
  - `database.py`: Database engine and session setup.
  - `models.py`: SQLAlchemy models for users, posts, votes.
  - `schemas.py`: Pydantic schemas for data validation (e.g., UserCreate, PostBase).
  - `routers/`: Modular routes for auth, posts, users, votes.
  - `oauth2.py`: JWT authentication logic.
  - `utils.py`: Utility functions like password hashing.
- `alembic/`: Migration files and scripts.

### Security

- Passwords are hashed with bcrypt.
- JWT tokens expire (configurable).
- Ownership checks prevent unauthorized actions.

### Development

- Run with `uvicorn app.main:app --reload`.
- Includes auto-generated API docs at `/docs`.

### Environment

- Requires Python 3.x and a running PostgreSQL server.
- Install dependencies with `pip install -r requirements.txt`.
