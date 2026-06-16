from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = SKILL_ROOT / "data"
CACHE_PATH = DATA_DIR / "skills_cache.json"
CUSTOM_RULES_PATH = DATA_DIR / "custom_rules.json"


def source_roots() -> list[dict[str, str]]:
    home = Path.home()
    cwd = Path.cwd()
    return [
        {
            "source": "user_agents_skills",
            "path": str(home / ".agents" / "skills"),
        },
        {
            "source": "project_agents_skills",
            "path": str(cwd / ".agents" / "skills"),
        },
        {
            "source": "codex_skills",
            "path": str(home / ".codex" / "skills"),
        },
        {
            "source": "plugin_cache",
            "path": str(home / ".codex" / "plugins" / "cache"),
        },
    ]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}

    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key in {"name", "description"}:
            metadata[key] = value
    return metadata


def detect_plugin_parts(skill_path: Path) -> dict[str, str]:
    parts = list(skill_path.parts)
    result = {"plugin": "", "provider": "", "version": ""}
    if "cache" not in parts:
        return result

    index = parts.index("cache")
    if len(parts) > index + 1:
        result["provider"] = parts[index + 1]
    if len(parts) > index + 2:
        result["plugin"] = parts[index + 2]
    if len(parts) > index + 3:
        result["version"] = parts[index + 3]
    return result


def read_custom_rules() -> dict:
    if not CUSTOM_RULES_PATH.exists():
        return {"rules": {}}
    try:
        return json.loads(CUSTOM_RULES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"rules": {}}


def discover_skills() -> dict:
    custom_rules = read_custom_rules().get("rules", {})
    skills = []
    scanned_roots = []

    for root_info in source_roots():
        root = Path(root_info["path"])
        exists = root.exists()
        scanned_roots.append(
            {
                "source": root_info["source"],
                "path": str(root),
                "exists": exists,
            }
        )
        if not exists:
            continue

        for skill_file in root.rglob("SKILL.md"):
            try:
                text = skill_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = skill_file.read_text(encoding="utf-8", errors="replace")

            metadata = parse_frontmatter(text)
            name = metadata.get("name") or skill_file.parent.name
            description = metadata.get("description", "")
            custom = custom_rules.get(name, {})
            plugin_parts = detect_plugin_parts(skill_file)

            skills.append(
                {
                    "id": f"{root_info['source']}:{name}:{len(skills) + 1}",
                    "name": name,
                    "description": description,
                    "path": str(skill_file),
                    "source": root_info["source"],
                    "plugin": plugin_parts["plugin"],
                    "provider": plugin_parts["provider"],
                    "version": plugin_parts["version"],
                    "known": bool(description or custom),
                    "custom_rule": bool(custom),
                    "custom": custom,
                }
            )

    return {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "cwd": os.getcwd(),
        "cache_path": str(CACHE_PATH),
        "scanned_roots": scanned_roots,
        "skill_count": len(skills),
        "skills": skills,
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CUSTOM_RULES_PATH.exists():
        CUSTOM_RULES_PATH.write_text(
            json.dumps({"rules": {}}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    cache = discover_skills()
    CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"skills_cache written: {CACHE_PATH}")
    print(f"skills discovered: {cache['skill_count']}")


if __name__ == "__main__":
    main()
