# second-brain

## Installation

Clone the repository and install dependencies:

```bash
git clone <repo-url>
cd second-brain
uv sync
```

## Usage

Via the CLI entrypoint:

```bash
uv run second_brain
uv run --env-file .env second_brain
```

Via Python module:

```bash
uv run python -m second_brain
```

## Environment Variables

Copy `.env.example` to `.env` for development defaults:

```bash
cp .env.example .env
```

| Variable    | Default    | Description                                          |
|-------------|------------|------------------------------------------------------|
| `LOG_LEVEL` | `INFO`     | Console log level — set to `DEBUG` in `.env` for verbose output |
| `LOG_FILE`  | `app.log`  | Path to the log file                                 |

Load dev environment explicitly with `uv run --env-file .env` (no auto-loading).

## Testing

```bash
uv run pytest
uv run pytest --cov
```

## Documentation

```bash
uv run python scripts/serve_docs.py   # preview locally
uv run mkdocs build                   # build static site
```
