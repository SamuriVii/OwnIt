# Contributing to OwnIt

All code, comments, commit messages, branch names, and PR descriptions must be written in **English**.

---

## Branches

```
feature/<short-description>     new functionality
fix/<short-description>         bug fix
refactor/<short-description>    code restructure, no behavior change
chore/<short-description>       tooling, deps, config, CI
docs/<short-description>        documentation only
test/<short-description>        tests only
```

Examples: `feature/user-auth`, `fix/redis-connection-timeout`, `chore/upgrade-fastapi`

Always branch off `main`. Keep branches short-lived — one concern per branch.

---

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>
```

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code change with no behavior change |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `chore` | Tooling, deps, config, CI |
| `perf` | Performance improvement |

**Rules:**
- Summary is lowercase, imperative mood, no trailing period
- Max 72 characters per line
- Reference issues when relevant: `fix(auth): handle expired token (#42)`

```bash
# Good
feat(health): add redis readiness endpoint
fix(session): rollback transaction on test teardown
chore(deps): upgrade sqlalchemy to 2.0.48

# Bad
Fixed the bug
WIP
updates
```

---

## Pull requests

- **One concern per PR** — do not mix features, fixes, and refactors
- **Title** follows Conventional Commits format: `feat(scope): summary`
- **Description** answers: what changed and why (not how — the code shows that)
- **Tests required** for every new endpoint, service, or utility function
- **No commented-out code** — delete it or don't commit it

Checklist:
- [ ] All quality gates pass (see service README for commands)
- [ ] New functionality has tests
- [ ] `.env.example` updated if new env variables added
- [ ] Migrations generated if models changed
- [ ] No secrets or credentials committed

---

## Code style

- **No comments that describe what the code does** — only why (non-obvious constraints, workarounds, invariants)
- **No docstrings on trivial functions** — the name and types are the documentation
- **Prefer explicit over implicit** — return types, type hints, no magic values

Tooling details and commands live in each service's `README.md`.
