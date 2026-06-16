# Codex Skill Router

Codex Skill Router is a lightweight Codex skill that helps route each task before substantial work begins. It decides which skills are relevant, whether Goal or Plan mode is safer, whether a read-only inspection should happen first, and whether multiple skills should be chained.

The router is designed to stay quiet for simple low-risk tasks. It becomes visible for complex or high-risk work such as browser automation, login workflows, database work, GitHub operations, config changes, file deletion, project scaffolding, or multi-file edits.

## Safety Model

For complex or high-risk tasks, Codex should:

- recommend Plan mode;
- start with read-only inspection;
- show recommended skills, risks, and boundaries;
- wait for explicit user approval before write actions;
- avoid creating, modifying, or deleting files before the plan is confirmed.

The router does not store credentials, modify Codex configuration, delete skills, disable plugins, or push to GitHub.

## Goal vs Plan

Use Goal mode for small, clear, low-risk tasks such as single-file fixes, direct explanations, small documentation edits, or narrowly scoped bug fixes.

Use Plan mode for new projects, multi-file changes, browser automation, login flows, database work, GitHub operations, config changes, deletion, cleanup tasks, or any task that needs read-only inspection before write actions.

## Repository Layout

```text
codex-skill-router/
├── README.md
├── LICENSE
├── .gitignore
├── skill-router/
│   ├── SKILL.md
│   └── scripts/
│       └── refresh_skills.py
└── examples/
    ├── custom_rules.example.json
    └── skills_cache.example.json
```

## Install

Copy the `skill-router/` directory into your Codex skills directory.

Typical locations:

- Windows: `%USERPROFILE%\.codex\skills\skill-router`
- macOS/Linux: `~/.codex/skills/skill-router`

Restart Codex or start a new session after installing the skill so the metadata is refreshed.

## Refresh Local Skill Cache

The refresh script scans local skill locations and writes a machine-local cache under `skill-router/data/`. That generated cache is intentionally ignored by Git.

From the installed skill directory:

```powershell
py skill-router/scripts/refresh_skills.py
```

or:

```bash
python skill-router/scripts/refresh_skills.py
```

The scanner checks:

- user-level `.agents/skills`;
- project-level `.agents/skills`;
- user-level `.codex/skills`;
- local Codex plugin cache.

## Custom Rules

Use `examples/custom_rules.example.json` as a template for machine-local custom rules.

After installing the skill, create:

```text
skill-router/data/custom_rules.json
```

Example:

```json
{
  "rules": {
    "my-local-skill": {
      "description": "What this local skill is for.",
      "keywords": ["keyword-a", "keyword-b"],
      "scenarios": ["When this skill should be recommended."],
      "priority": 60
    }
  }
}
```

Do not commit real `custom_rules.json` files if they contain private project names, paths, or local workflow details.

## Example Routing Output

For simple low-risk tasks, routing can stay silent.

For complex or high-risk tasks, Codex should show a short summary:

```text
Routing:
- Mode: Plan
- Skills: skill-a -> skill-b
- Read-only first: yes
- Risk flags: config change, browser automation
- Boundary: inspect first; do not modify/delete/push until plan is confirmed
```

## Do Not Commit

Do not publish:

- generated `skills_cache.json`;
- machine-local `custom_rules.json`;
- backup files;
- Codex `config.toml`;
- plugin cache directories;
- credentials, tokens, or private workspace paths.

The included `.gitignore` blocks these by default.

## License

MIT License.
