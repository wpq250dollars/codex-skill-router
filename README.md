# codex-skill-router

Codex Skill Router is a lightweight Codex skill that helps route each task before substantial work begins. It decides which skills are relevant, whether Goal or Plan mode is safer, whether read-only inspection should happen first, and whether multiple skills should be chained.

codex-skill-router 是一个轻量级 Codex Skill，用来在正式执行任务前做“路由判断”：当前任务适合哪些 skills，应该走 Goal 还是 Plan，是否需要先只读检查，以及是否需要多个 skills 串联。

## What is this? / 这是什么？

Codex Skill Router is a meta skill for task triage. It does not solve the task directly; it helps Codex choose a safer and more suitable execution path first.

这是一个“元 skill”，重点不是直接完成某个具体任务，而是帮助 Codex 先判断任务类型和执行边界，再决定后续怎么做。

It is designed to stay quiet for simple low-risk tasks and become visible for complex or high-risk work.

对于简单、低风险任务，它应该尽量保持安静；对于复杂或高风险任务，它会显示推荐模式、推荐 skills、风险边界和只读检查要求。

## Why use it? / 为什么需要它？

Codex can use many skills, tools, and workflows. Without a routing step, it may move too quickly into implementation, especially for tasks involving browser automation, login flows, database work, GitHub operations, config changes, deletion, or multi-file edits.

Codex 可以使用很多 skills、工具和工作流。如果没有前置路由判断，它可能在浏览器自动化、登录流程、数据库、GitHub 操作、配置修改、删除文件或多文件改动这类任务中过早进入执行。

This skill adds a small safety gate: simple work stays fast, while complex work gets a short plan and explicit user confirmation before write actions.

这个 skill 的作用是加一道轻量安全闸门：简单任务不变慢，复杂任务先给出简短计划和边界，等用户确认后再写文件或执行高风险操作。

## Features / 功能特性

- Select relevant Codex skills for a task.
- Recommend Goal mode or Plan mode.
- Detect high-risk operations.
- Recommend read-only inspection before write actions.
- Suggest multi-skill workflows when one skill is not enough.
- Keep routing silent for simple low-risk tasks.
- Provide a local skill cache refresh script.

- 为任务推荐合适的 Codex skills。
- 判断应该使用 Goal 模式还是 Plan 模式。
- 识别高风险操作。
- 在写入或执行前建议先做只读检查。
- 当单个 skill 不够时，推荐多 skill 串联。
- 对简单低风险任务保持静默，不输出冗余分析。
- 提供本地 skills 缓存刷新脚本。

## Installation / 安装方法

Copy the `skill-router/` directory into your Codex skills directory.

将 `skill-router/` 目录复制到你的 Codex skills 目录。

Typical locations:

常见安装位置：

- Windows: `%USERPROFILE%\.codex\skills\skill-router`
- macOS/Linux: `~/.codex/skills/skill-router`

Restart Codex or start a new session after installing the skill so the metadata is refreshed.

安装后重启 Codex，或新开一个会话，让 Codex 重新加载 skill 元数据。

## Usage / 使用方法

Once installed, Codex can use the router as a default pre-task check. You normally do not need to invoke it manually.

安装后，它可以作为 Codex 的默认前置判断逻辑使用。一般情况下，你不需要每次手动说“调用 skill-router”。

For simple tasks, routing can remain silent. For complex or high-risk tasks, Codex should show a short routing summary:

简单任务可以静默路由；复杂或高风险任务应显示简短路由摘要：

```text
Routing:
- Mode: Plan
- Skills: skill-a -> skill-b
- Read-only first: yes
- Risk flags: config change, browser automation
- Boundary: inspect first; do not modify/delete/push until plan is confirmed
```

## Goal vs Plan / Goal 与 Plan 模式

Use Goal mode for small, clear, low-risk tasks such as single-file fixes, direct explanations, small documentation edits, or narrowly scoped bug fixes.

Goal 模式适合小范围、目标明确、风险较低的任务，例如单文件修复、直接解释、小型文档修改，或边界清楚的 bug 修复。

Use Plan mode for new projects, multi-file changes, browser automation, login flows, database work, GitHub operations, config changes, deletion, cleanup tasks, or any task that needs read-only inspection before write actions.

Plan 模式适合新项目、多文件修改、浏览器自动化、登录流程、数据库操作、GitHub 操作、配置修改、删除文件、清理任务，或任何需要先只读检查再写入的任务。

## Safety Rules / 安全规则

For complex or high-risk tasks, Codex should:

对于复杂或高风险任务，Codex 应该：

- recommend Plan mode;
- start with read-only inspection;
- show recommended skills, risks, and boundaries;
- wait for explicit user approval before write actions;
- avoid creating, modifying, deleting, pushing, or releasing before the plan is confirmed.

- 推荐 Plan 模式；
- 先进行只读检查；
- 展示推荐 skills、风险点和执行边界；
- 在写入操作前等待用户明确确认；
- 在计划确认前，不创建、不修改、不删除、不 push、不发布 release。

The router does not store credentials, modify Codex configuration, delete skills, disable plugins, or push to GitHub.

这个 router 不保存凭据，不修改 Codex 配置，不删除 skills，不禁用插件，也不会自动 push 到 GitHub。

## Refresh Skills Cache / 刷新 Skills 缓存

The refresh script scans local skill locations and writes a machine-local cache under `skill-router/data/`. That generated cache is intentionally ignored by Git.

刷新脚本会扫描本机可用的 skills，并把机器本地缓存写入 `skill-router/data/`。这个生成目录默认会被 Git 忽略，不应该提交。

From the installed skill directory:

在安装后的 skill 目录中运行：

```powershell
py skill-router/scripts/refresh_skills.py
```

or:

或者：

```bash
python skill-router/scripts/refresh_skills.py
```

The scanner checks:

扫描范围包括：

- user-level `.agents/skills`;
- project-level `.agents/skills`;
- user-level `.codex/skills`;
- local Codex plugin cache.

- 用户级 `.agents/skills`；
- 项目级 `.agents/skills`；
- 用户级 `.codex/skills`；
- 本地 Codex 插件缓存。

## Custom Rules / 自定义规则

Use `examples/custom_rules.example.json` as a template for machine-local custom rules.

可以使用 `examples/custom_rules.example.json` 作为模板，创建只保存在本机的自定义规则。

After installing the skill, create:

安装后可以创建：

```text
skill-router/data/custom_rules.json
```

Example:

示例：

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

如果真实的 `custom_rules.json` 包含私有项目名、本机路径或个人工作流细节，不要提交到仓库。

## Examples / 示例

Simple low-risk task:

简单低风险任务：

```text
Explain this function.
```

Expected behavior: Codex can route silently and answer directly.

预期行为：Codex 可以静默路由，直接回答。

Complex or high-risk task:

复杂或高风险任务：

```text
Build a browser automation helper that logs in and saves task data locally.
```

Expected behavior: Codex should recommend Plan mode, start with read-only inspection, show safety boundaries, and wait for approval before creating or modifying files.

预期行为：Codex 应推荐 Plan 模式，先只读检查，展示安全边界，并在创建或修改文件前等待用户确认。

Multi-skill task:

多 skill 串联任务：

```text
Turn a PDF report into a slide deck.
```

Expected behavior: Codex may recommend chaining `pdf` and `presentations`.

预期行为：Codex 可以推荐串联 `pdf` 和 `presentations`。

## What not to commit / 不应提交的文件

Do not publish:

不要发布以下内容：

- generated `skills_cache.json`;
- machine-local `custom_rules.json`;
- backup files;
- Codex `config.toml`;
- plugin cache directories;
- credentials, tokens, or private workspace paths.

- 生成的 `skills_cache.json`；
- 机器本地的 `custom_rules.json`；
- 备份文件；
- Codex `config.toml`；
- 插件缓存目录；
- 凭据、token 或私有工作区路径。

The included `.gitignore` blocks these by default.

仓库中的 `.gitignore` 已默认屏蔽这些文件。

## License / 许可证

MIT License.

本项目使用 MIT License。
