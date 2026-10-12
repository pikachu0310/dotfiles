---
name: web-design-guidelines
description: Review user-facing web UI for accessibility, interaction, performance, and UX issues against a pinned Web Interface Guidelines snapshot. Use when asked to review UI, accessibility, UX, or frontend quality.
---

# Web design guidelines

Review the real target files and, when available, the rendered interface. Read `references/web-interface-guidelines.md` completely before issuing findings.

## Review workflow

1. Identify the files, routes, viewport range, and user journey in scope.
2. Inspect repository-specific design and accessibility rules before the shared guideline snapshot.
3. Observe the rendered surface when visual or interactive behavior matters.
4. Report only reproducible, user-impacting findings. Include a precise file and line when source location is known.
5. Separate verified defects from items that still require browser, device, screen-reader, or human validation.

Rank findings by impact. Explain the broken user outcome and the smallest credible correction; avoid dumping every guideline as a checklist.

## Snapshot boundary

The bundled reference is pinned for reproducibility. Do not fetch or execute mutable remote instructions during an ordinary review. Update the snapshot only when the user explicitly asks to refresh this Skill, then re-check its source, revision, license, and behavior before replacing it.

Do not edit files when the request is review-only. Do not describe an unobserved visual result as verified.
