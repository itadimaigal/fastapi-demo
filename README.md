# itadimaigal — FastAPI course: working examples

The code from Professor SK's video **"FastAPI Full Course: Build a Real Python API from Scratch"**.

It has two parts:

- **`examples/`** — four small, single-file apps, one for each step of the video.
- **`app/`** — a complete **Expense Tracker API**: users, login with JWT tokens, a SQLite database,
  create / list / filter / update / delete expenses, a spending summary, tests, Docker and CI.

## What's inside

```
examples/
  01_hello.py        your first endpoints
  02_params.py       path and query parameters, validation
  03_body.py         request bodies (Pydantic), response models, status codes, in-memory CRUD
  04_async.py        async endpoints and background tasks
app/
  main.py            creates the app, CORS, routers, startup
  config.py          settings from environment variables / .env
  database.py        SQLModel engine and the get_session dependency
  models.py          database tables and request/response schemas
  security.py        password hashing (Argon2), JWT tokens, get_current_user
  routers/auth.py    POST /auth/register, POST /auth/token, GET /auth/me
  routers/expenses.py  CRUD + GET /expenses/summary
tests/               16 tests with pytest and FastAPI's TestClient
Dockerfile           production container
.github/workflows/ci.yml   lint + tests (Python 3.12 and 3.13) + Docker build check
```

## 1. Set up (Windows, macOS or Linux)

Needs **Python 3.12 or newer**.

```bash
python -m venv .venv
```

Activate it — Windows: `.venv\Scripts\activate` · macOS/Linux: `source .venv/bin/activate`

```bash
pip install -r requirements-dev.txt
```

## 2. Run the step-by-step examples

```bash
fastapi dev examples/01_hello.py
```

Open http://127.0.0.1:8000 and the interactive docs at **http://127.0.0.1:8000/docs**.
Stop it with Ctrl+C, then try `02_params.py`, `03_body.py` and `04_async.py` the same way.

## 3. Run the Expense Tracker API

```bash
fastapi dev app/main.py
```

In http://127.0.0.1:8000/docs:

1. **POST /auth/register** — create a user, e.g. `{"username": "asha", "password": "secret-pass-123"}`
2. Click **Authorize** (top right), enter the same username and password, and log in.
3. **POST /expenses** — add some expenses, e.g. `{"title": "Team lunch", "amount": 850, "category": "food"}`
4. **GET /expenses?category=food**, **GET /expenses/summary**, **PATCH** and **DELETE** them.

The data is stored in `expenses.db` (SQLite) in the project folder.

## 4. Run the tests

```bash
pytest -v
ruff check .
```

## 5. Configuration

Settings come from environment variables or a `.env` file. Copy `.env.example` to `.env` and change it.
**Always set your own long, random `SECRET_KEY` in production**, for example:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

To use PostgreSQL instead of SQLite, set
`DATABASE_URL=postgresql+psycopg://user:password@host/dbname` and `pip install "psycopg[binary]"`.

## 6. Run it with Docker

```bash
docker build -t expense-api .
docker run -p 8000:8000 -e SECRET_KEY=your-long-random-secret -v expense-data:/app/data expense-api
```

The `-v expense-data:/app/data` volume keeps the database when the container is replaced.

## 7. CI on GitHub

Push this repository to GitHub and open the **Actions** tab: `CI` lints the code, runs the tests on
Python 3.12 and 3.13, then builds the Docker image and checks `/health`.
(See the itadimaigal GitHub Actions video for how this works.)

## Try it yourself

- Add a `note` field to expenses (model → test → endpoint).
- Add `GET /expenses?from_date=...&to_date=...`.
- Add a monthly budget per category and warn when it is exceeded.

## Versions

Tested with FastAPI 0.162, Pydantic 2.14, SQLModel 0.0.48 and Python 3.13. The exact versions are
pinned in `requirements.txt`, so the examples keep working even as new versions come out.
