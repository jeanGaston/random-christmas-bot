# Agent instructions for this repository

This file guides both human contributors and AI coding agents working in this
repo. Follow it unless the user explicitly asks for something different.

## Branching model

- `main` — always deployable. Only receives finished, working changes.
- `dev` — integration branch for in-progress work (new features, larger
  refactors, anything not yet proven). Merge to `main` only once it works.
- Feature branches (optional): `feature/<short-name>` or `fix/<short-name>`
  cut from `dev` for anything that touches multiple files or takes more than
  one sitting. Small, obvious fixes can go straight to `dev`.

Rebase feature branches on `dev` before opening a PR/merge if `dev` has moved
on; don't merge `dev` into `main` with unresolved conflicts.

## Commit practices

- Commit early and often — one logical change per commit. Don't bundle an
  unrelated refactor with a bug fix.
- Write commit messages in the imperative mood ("Add exclusion support", not
  "Added" or "Adding"), with a short summary line (~50-70 chars) and, if
  needed, a blank line followed by bullet points explaining *why*.
- Never commit secrets: SMTP credentials, real participant CSV paths, API
  keys. Real configuration lives in a local `.env` file (gitignored) —
  `env.py` only reads `os.environ`/`.env` and must never hardcode real values.
  If you add a new secret, add its placeholder to `.env.example` too.
- Before committing, check `git status` and `git diff` for anything
  unexpected (stray debug prints, personal file paths, credentials).
- Prefer creating new commits over amending, unless explicitly asked to amend
  and the previous commit hasn't been pushed/shared.
- Don't use `--no-verify`, force-push, or rewrite shared history without
  explicit user approval.
- Run whatever tests/scripts are relevant before committing (`src/test_draws.py`
  for conflict checks; manually exercise `main.run_draw()` or the web GUI for
  behavior changes — there's no CI yet).

## Code style

- Keep the existing flat-module layout in `src/` (`draw.py`, `file_io.py`,
  `emailer.py`, `env.py`, `main.py`, `utils.py`); they import each other with
  plain `from x import y`, so `src/` must stay on `sys.path` for anything that
  imports them (see `webapp/app.py` for how the web GUI does this).
- No comments explaining *what* code does — only *why*, when it's non-obvious
  (e.g. a workaround, an invariant, a subtle constraint).
- Don't add abstractions, config flags, or error handling for cases that
  can't happen. Keep changes scoped to what was asked.
- Type hints are used inconsistently today (see `utils.py` vs `file_io.py`);
  match the style of the file you're editing rather than mixing conventions.

## Secrets & data

- `.env` (real secrets, gitignored) vs `.env.example` (committed template) —
  keep them in sync whenever a new config key is added.
- Participant CSV data lives outside the repo (`CSV_PATH`), never commit
  sample data containing real names/emails.
- The web GUI can trigger real emails to real people via `run_draw()` — treat
  "run draw" as a destructive/one-way action (it also overwrites this year's
  CSV) and confirm with the user before wiring up anything that calls it
  automatically (e.g. a cron/scheduled container).

## Deployment

- `Dockerfile` builds the web GUI service; `docker-compose.yml` wires it up
  with a volume for `CSV_PATH` and an `.env` file for config. See the
  README's Docker section for usage.
