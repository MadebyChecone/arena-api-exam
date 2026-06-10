# ArenaAPI

A small FastAPI tournament backend. Your job: audit, fix, secure, and test it.

## ⚠️ Read this first

- **Edit only `app/`.** Never change `AGENTS.md`, `CLAUDE.md`, or anything under
  `grader/`. You may *read* anything and *run* the commands below.
- **The exam subject is in [`docs/`](docs).** Read it before you start.
- **Windows users: run everything in Git Bash** (ships with Git for Windows).
  It provides `make`. Plain cmd/PowerShell do not.

## Setup

```bash
# Create and use Python virtualenv
python -m venv .venv
source .venv/bin/activate    # Windows (Git Bash): source .venv/Scripts/activate

make install                 # Install dependencies
make seed                    # Initialize database with fake data
make run                     # Start FastAPI dev server
```

All `make` commands assume an activated virtualenv.

## Commands
- **`make help`**: show all the commands with a help message.
- **`make seed`**: fill the local database with demo data.
- **`make run`**: start the API with auto-reload at http://localhost:8000
  (web UI at `/`, interactive API docs at `/docs`).
- **`make test`**: run the test suite.
- **`make black`**: format `app/` with Black.
- **`make criteria`**: print the graded criteria (the spec to satisfy).
- **`make grade`**: compute your score locally.

## Formatting

The only authorized formatter for this project is **Black**. Do not use other
auto-formatters or broad IDE reformatting.

```bash
make black
```

This formats the editable application code in `app/`.

## Reset everything

If the data gets into a weird state:

```bash
rm arena.db        # delete the database
make seed          # recreate + refill it
```

Then **restart the dev server** (`make run`); it won't pick up the new
database otherwise.

## Project structure

```
app/            the only code you edit
  api/          HTTP endpoints (thin FastAPI routers)
  logic/        business logic (ELO, brackets, tournament rules)
  web/          server-rendered UI (templates + static assets)
  models.py     database tables       database.py   DB setup
  main.py       app entrypoint        seed.py       demo data
  tests/        your tests
grader/         grading system, DO NOT EDIT
docs/           the exam subject
```

## Grading

Run **`make criteria`** to see the spec you must satisfy, and **`make grade`**
to compute your score locally at any time.

On every push, GitHub also recomputes your grade: open your repo, go to the
**Actions** tab, then the latest run summary. [Open the Actions tab](../../actions).
</content>
</invoke>
