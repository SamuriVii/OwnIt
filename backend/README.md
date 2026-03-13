# OwnIt - Backend API 🚀

A sleek and powerful self-management API built with **FastAPI** and **Python 3.13**.
This project uses a Makefile-first workflow for dev tasks (running tests, linting, type-check, migrations, dependencies).  
All documentation is in English.

---

## 📦 Prerequisites

- Docker + Docker Compose (for containerized local dev)
- `uv` (recommended package manager, used in Makefile)
- `make`
- Python 3.13 (inside the container / local environment)

> Use `uv` instead of `pip` for dependency management in this project.

---

## 🚀 Local development start (container)
Make sure that the main repository is running.

```bash
cd /OwnIt
docker compose -f docker-compose.dev.yml up --build
```

API endpoints:
- http://localhost:8000
- Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

---

## 🖥️ Preferred VS Code workflow (WSL2 + Dev Container)

1. Open the repo from WSL workspace path (`/OwntIt/backend`) in VS Code.
2. Use command palette (`Ctrl+Shift+P`) and run `Remote-WSL: Reopen Folder in WSL`.
3. Then run `Dev Containers: Reopen in Container` (target `ownit-backend-dev` container).
4. Inside container terminal run project commands e.g. `make test`, `make migrate`.

---

## 🔧 Developer workflow (Makefile-first)

Most commands should be run inside the container shell once it is up.
Use `make <target>` for everything.

### All available commands (cheat sheet)

| Make target | Purpose | Equivalent commands |
|------------|---------|----------------------|
| `make help` | Show all available targets | `make help` |
| `make add p=<package>` | Add production dependency | `uv add <package>` |
| `make add-dev p=<package>` | Add dev dependency | `uv add --group dev <package>` |
| `make migrations m="name"` | Auto-generate alembic migration | `alembic revision --autogenerate -m "name"` |
| `make migrate` | Apply migrations | `alembic upgrade head` |
| `make rollback` | Roll back last migration | `alembic downgrade -1` |
| `make history` | Show migration history | `alembic history --verbose` |
| `make current` | Show current migration | `alembic current` |
| `make test` | Run pytest | `pytest` |
| `make test-v` | Run pytest with logs | `pytest -s` |
| `make lint` | Ruff lint check | `ruff check .` |
| `make format` | Ruff format | `ruff format .` |
| `make type-check` | Mypy type check | `mypy .` |
| `make check-all` | format + lint + type-check + tests | (chained) |
| `make clean` | remove caches and coverage artifacts | cleanup dirs |

---

## 🧪 Quality commands

Use `make` for consistency:

```bash
make test          # run tests
make test-v        # run tests with visible logs
make lint          # ruff static checks
make format        # ruff formatting
make type-check    # mypy check
make check-all     # all quality gates
```

---

## 🗄 Database and Alembic

Always run migration workflow after model/schema updates (`app/models/`).

```bash
make migrations m="add field X"
make migrate
```

Roll back a single revision:

```bash
make rollback
```

Use these for inspection:

```bash
make history
make current
```

---

## 🌐 IDE / VS Code Recommendations

Recommended VS Code extensions:
- Dev Containers (Microsoft)
- Python (Microsoft)
- Ruff (Astral)
- Mypy (if available) or Python type-checking support
- Even Better Toml
- PostgreSQL / Database Client extension (e.g., `PostgreSQL` by Chris Kolkman)

> Dev Containers can automatically install workspace recommended extensions and tooling from `.devcontainer/devcontainer.json`. If some extension is missing, install it manually in the container.

### Database Client setup

- Prefer auto-magic connection from `.env` variable (if extension supports it)
- Or configure connection URL manually from `.env`:
  - `DATABASE_URL=postgresql://user:pass@host:port/dbname`

---

## 📁 Project structure

- `app/` : main FastAPI application code (controllers, routes, business logic)
- `tests/` : pytest test suite
- `alembic/` : DB migration scripts + config
- `.devcontainer/` : container setup (Dev Container definitions)
- `alembic.ini` : alembic settings
- `Dockerfile.dev` : dev container image
- `pyproject.toml` : central tooling configuration (ruff, mypy, pytest)
- `Makefile` : developer CLI workflow
- `uv.lock` : locked dependency graph

---

## 🔁 Dependency management

Install all dependencies using `uv`:

```bash
uv install
```

Add packages from Makefile:

```bash
make add p=requests
make add-dev p=pytest
```

---

## 📝 Notes

- Keep README and workflows in sync with Makefile.
- Use `make *` for deterministic and low-cognitive effort commands.
- `uv` replaced direct `pip` usage, per project policy.

