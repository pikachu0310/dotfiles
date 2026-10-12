---
name: git-commit-style-gitmoji
description: Write concise Git commit messages with one Gitmoji that represents the primary intent. Use when the user or repository explicitly requests Gitmoji-style commits or commit-message suggestions.
---

# Gitmoji commit style

Follow the repository's commit rules first. Use this style only when Gitmoji is requested or already established by the project.

## Compose the message

1. Inspect the staged or intended diff before choosing an emoji.
2. Choose one emoji for the primary intent. Do not stack several emojis to summarize unrelated changes.
3. Add a short scope only when it helps distinguish the affected area.
4. Write a concrete, imperative summary in the language used by the repository.
5. Add a body only when the reason, migration, compatibility impact, or verification would otherwise be lost.

Use this shape:

```text
<emoji> [(scope)]?: <imperative summary>
```

Examples:

```text
✨ intent: add the public intake workflow
🐛 bootstrap: preserve existing context files
📝 document the Windows and WSL boundary
```

Read `references/gitmojis.json` when the appropriate emoji is uncertain. Prefer the entry whose intent matches the change; do not choose by appearance alone.

## Guardrails

- Keep one coherent outcome per commit.
- Do not claim tests, fixes, migrations, or releases that did not happen.
- Do not include secrets, private paths, task IDs, or issue references that are not already public.
- Do not amend, commit, or push merely because a message was requested.
