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