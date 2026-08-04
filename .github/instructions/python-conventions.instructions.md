---
description: "Use when writing or editing Python (*.py) in this repo. Enforces PEP 8 and the coding conventions demonstrated in docs/example.py (type hints, PEP 604 unions like 'str | None', trailing commas, timezone-aware UTC datetimes, and readable comprehensions)."
applyTo: "**/*.py"
---
# Python Conventions (PEP 8 + this repo)

- Follow PEP 8: clear naming, small functions, consistent formatting.
- Add a short module docstring at the top of each file describing purpose/context.
- Use type hints for all function inputs and outputs.
- Prefer PEP 604 union types over `typing.Optional` (e.g., `str | None`, `datetime.datetime | None`).
- Add docstrings for public functions/classes and describe inputs/outputs (e.g., `:param name: description` / `:return: description`).
- Call functions with keyword arguments when it improves clarity (e.g., `create_user(name="Alice", age=30)`).
- Prefer English identifiers in code; use Danish only when a concept can’t reasonably be translated, and explain briefly.
- Use short inline comments to explain non-obvious lines/choices; avoid commenting the obvious.
- Naming: classes in `PascalCase`, functions/variables in `snake_case`.
- Boolean naming: prefer `is_`, `has_`, `can_` prefixes.
- Private helpers: prefix with `_`.
- Prefer dataclasses/classes over raw dictionaries for structured data, especially for parameters.
- Logging: minimize non-error logs; use `logger.debug(...)` for non-critical diagnostic info.

- Use timezone-aware UTC timestamps: `datetime.datetime.now(datetime.timezone.utc)` (avoid `datetime.datetime.utcnow()`).
- Use trailing commas in multiline literals and argument lists.
  - Example:
    - `config = {"a": 1, "b": 2,}` when written across multiple lines.
- Prefer simple comprehensions over unnecessary list/set/dict constructions.
  - Example: prefer `{f(x) for x in xs}` over `set([f(x) for x in xs])`.

Keep examples minimal and readable; avoid clever one-liners if they hurt clarity.

# Tools for formatting and linting
- Call `autopep8` to automatically format code according to PEP 8.
- Use `isort` to keep imports organized and consistent.
- Use `flake8` to check for style issues and enforce conventions.

# Dependency suggestions:
- For managed oauth2, database management and email handling, suggest using `rk-digi` python package.
