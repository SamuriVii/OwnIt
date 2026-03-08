# OwnIt - Backend API 🚀

A sleek and powerful self-management API built with **FastAPI** and **Python 3.13**.
This service handles the core logic, data management, and personal growth tracking for the OwnIt application.

---

## 🛠 Development Environment

The project is fully containerized to ensure environment consistency across different machines.
We use **WSL2** and **Docker** for the development workflow.

---

## 🚀 Quick Start (Dev Mode)

To spin up the development environment, run the following command from the **root directory** of the project:

```bash
docker compose -f docker-compose.dev.yml up --build
```

### API Endpoints

- **API URL:** [http://localhost:8000](http://localhost:8000)  
- **Interactive API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)  
- **Alternative Docs (Redoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 💻 Recommended Setup (Cursor / VS Code)

To get the best developer experience (IntelliSense, linting, debugging), we highly recommend using the Dev Containers workflow to connect directly to the running container.

### 1️⃣ Essential Extensions

Install these inside your editor to work seamlessly with the containerized Python environment:

- **Dev Containers (Microsoft)** – Connects your editor to the running Docker container  
- **Python (Microsoft)** – Core support for Python 3.13  
- **Python Debugger** – Enables setting breakpoints inside the container  
- **Ruff (Astral)** – Extremely fast linting & formatting  
- **Mypy Type Checker** – Strict static type checking  
- **Even Better TOML** – Syntax highlighting and validation for `pyproject.toml`

---

### 2️⃣ Connecting to the Container

1. Ensure the containers are running:

```bash
docker compose -f docker-compose.dev.yml up
```

1. Click the **Remote Window icon** (bottom-left corner of Cursor) or press `Ctrl+Shift+P`
2. Select **"Reopen in Container..."**
3. Choose `ownit-backend-dev`
4. Once connected, open the `/app` folder inside the container

---

## 🗄️ Database Migrations (Alembic)

This project uses **Alembic** for database schema management. Whenever you modify a model in the `app/models/` directory, you need to generate and apply a migration.

### 🔄 Your Daily Workflow

When you change the database schema (e.g., adding a new column in `models/users.py`), follow these steps inside the container terminal:

1. **Generate a migration script:**
   ```bash
   alembic revision --autogenerate -m "change description"
   ```
2. **Synchronize the DEV database:**
   ```bash
   alembic upgrade head
   ```

### 🛠️ Useful Alembic Commands

| Task                 | Command                     | Description                     |
| -------------------- | --------------------------- | ------------------------------- |
| Apply all migrations | `alembic upgrade head`      | Brings DB to the latest version |
| Rollback 1 version   | `alembic downgrade -1`      | Reverts the last migration      |
| View history         | `alembic history --verbose` | Lists all applied migrations    |
| Current state        | `alembic current`           | Shows the current DB revision   |

---

## 🧪 Quality Control & Testing

All tools are pre-configured in `pyproject.toml`.

Run these commands inside the container terminal:


| Task        | Command         | Description                                    |
| ----------- | --------------- | ---------------------------------------------- |
| Run Tests   | `pytest`        | Runs the test suite with coverage report       |
| Lint Check  | `ruff check .`  | Checks for logical errors and style violations |
| Format Code | `ruff format .` | Automatically formats code to PEP8 standards   |
| Type Check  | `mypy .`        | Runs strict type analysis                      |


---

## 📦 Dependency Management

This project uses `pyproject.toml` as the single source of truth for dependencies.

To update your environment after adding new packages:

```bash
pip install -e ".[dev]"
```

> **Note:** Major changes to dependencies may require a container rebuild using the `--build` flag.

---

## 📝 Project Structure Highlights

- `/app` – Main application code  
- `/tests` – Pytest suite  
- `pyproject.toml` – Modern Python project configuration (Ruff, Mypy, Pytest)  
- `Dockerfile.dev` – Optimized development container image

