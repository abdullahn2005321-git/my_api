# my_api

Flask REST API with JWT authentication and SQLite.

## What This Project Includes

- Authentication: register, login, and current-user endpoint (`/me`)
- Users CRUD API
- Pagination, sorting, and name filtering for users list
- SQLite setup with automatic table initialization

## Tech Stack

- Python 3.10+
- Flask
- Flask-JWT-Extended
- SQLite

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Server default:

- `http://127.0.0.1:5000`

## Environment Variables

- `JWT_SECRET_KEY`: JWT signing key
- `DB_PATH`: SQLite file path (default: `app.db`)

Windows example:

```bash
set JWT_SECRET_KEY=replace-with-a-strong-secret
set DB_PATH=app.db
```

## Endpoints

### System

- `GET /` simple welcome response
- `GET /health` health check

### Auth

- `POST /register`
- `POST /login`
- `GET /me` (JWT required)

Register/Login body:

```json
{
  "username": "abdullah",
  "password": "1234"
}
```

Use token:

```http
Authorization: Bearer <token>
```

### Users

- `GET /users?name=&sort=asc&page=1&limit=5`
- `POST /users`
- `GET /users/<id>`
- `PUT /users/<id>`
- `DELETE /users/<id>`

Create/Update body:

```json
{
  "name": "Ali"
}
```

## Project Structure

- `app.py`: app setup + auth routes
- `users_routes.py`: users CRUD blueprint
- `db.py`: DB connection and schema initialization
- `wsgi.py`: WSGI entrypoint
- `tests/`: API tests

## Security Notes

- Do not use development JWT secrets in production.
- Keep `app.db` out of Git for real deployments.
