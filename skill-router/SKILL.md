---
name: "skill-router"
description: "skill selection, goal, plan, high-risk task detection, browser automation, login workflow, config changes, GitHub operations, database work, project scaffolding, multi-skill workflow. Use to decide which Codex skills to use, whether Goal or Plan mode is appropriate, whether read-only inspection is needed, and how to chain multiple skills safely."
---

# Skill Router

Use this skill as a default routing layer before substantial Codex work. Keep routing silent for simple low-risk tasks. Show a routing summary only when the task is complex, ambiguous, multi-skill, or high-risk.

## Core Decisions

Decide these before acting:

- Relevant skills to use.
- Goal mode or Plan mode.
- Whether multiple skills should be chained.
- Whether read-only inspection must happen first.
- Whether the task contains high-risk operations.

## Silent vs Visible Routing

Use silent routing when the task is simple, low-risk, and clearly scoped, such as small edits, explanations, one-file bugs, or direct questions.

Show a short routing summary when any of these apply:

- New project, architecture, scaffolding, or multi-file implementation.
- Browser automation, login, account/session workflow, or screenshots.
- Database, Supabase, migration, auth, RLS, production data, or schema changes.
- GitHub PR, issue, CI, push, release, publish, or deployment.
- Config, environment variables, secrets, credentials, or system settings.
- Deleting files, moving many files, cleanup, reset, overwrite, or destructive operations.
- Multiple skills are likely needed.
- The user explicitly asks for planning, safety boundaries, or skill selection.

## Mode Selection

Recommend Goal mode for low-risk work:

- Small clear fixes.
- Single-file or narrow changes.
- Clear bug with direct reproduction.
- No account, browser, database, config, GitHub write, deletion, or release risk.

Recommend Plan mode for higher-risk or broader work:

- New project or multi-file design.
- Architecture decisions.
- Browser automation, login, or account actions.
- Database work, migrations, Supabase, RLS, auth, or production data.
- Config changes, environment variables, secrets, credentials, or tool setup.
- GitHub operations, CI debugging, PR review, push, release, or deployment.
- File deletion, cleanup, reset, bulk moves, or overwrite operations.

If a task includes deletion, config/env changes, login, browser automation, database work, GitHub push/release, or deployment, recommend Plan mode and start with read-only inspection.

Complex/high-risk tasks must stop after plan/read-only inspection and wait for explicit user approval before write actions.

## Skill Matching

Prefer discovered skills from `data/skills_cache.json` when available. Use `data/custom_rules.json` to improve unknown or local skills. If the cache is missing or stale, ask to run the refresh script from the installed skill directory:

```bash
python skill-router/scripts/refresh_skills.py
```

Use common pairings:

- PDF to slides: `pdf` then `presentations`.
- Spreadsheet or CSV analysis: `spreadsheets` and, for analytical decisions or dashboards, `data-analytics`.
- GitHub PR or CI: `github`, then `gh-fix-ci` or `gh-address-comments` when relevant.
- OpenAI API app: `openai-platform-api-key`, then `openai-docs` or OpenAI developer skills.
- Supabase or Postgres: `supabase`, then `supabase-postgres-best-practices` for SQL/schema/performance.
- Browser testing or local web UI: `browser` or `playwright-interactive`.
- Desktop app automation: `computer-use` or `electron` when applicable.

If a discovered skill has no registry/custom explanation, mark it as unknown, keep it visible as a candidate, and suggest adding metadata to `data/custom_rules.json`.

## Visible Output Template

For complex or high-risk work, keep the summary short:

```text
Routing:
- Mode: Plan
- Skills: skill-a -> skill-b
- Read-only first: yes
- Risk flags: config change, browser automation
- Boundary: inspect first; do not modify/delete/push until plan is confirmed
```

Then continue according to the active collaboration mode and user instructions.
