# Design lineage

This local skill was deliberately adapted instead of installing several overlapping workflows.

- OpenAI Codex best practices: one coherent outcome per chat, durable repository guidance, and worktrees for parallel edits.
- ECC `search-first`: inspect existing solutions before writing custom code and choose among adopt, extend, compose, or build.
- COMPASS `task-clarifier`: ask only outcome-changing questions and make the user's decisions explicit.
- Superpowers `brainstorming`: obtain alignment before creative implementation.

The local version omits mandatory subagents, mandatory design documents and commits, exhaustive clarification for every request, and automatic profile maintenance. Those behaviors would add ceremony or context state beyond pikachu0310's intended boundary.

## 2026-10-11 owner-authorized refinement

The owner selected A for relevant-history retrieval, skill synchronization, concise always-read guidance, and evidence-led cause investigation; Context7 and extra PR workflow were declined.

- [motoki317/dotfiles code rules](https://github.com/motoki317/dotfiles/blob/8ef01ade3e5c8c740842b53a599b6ae4a2709870/.claude/rules/code.md): reuse existing code, standard functions, and installed dependencies before adding abstractions; preserve requested quality and identify the state owner.
- The upstream investigation workflow informed the distinction between an observation and a competing cause, but this adaptation does not require three hypotheses, separate agents, a handoff, or a written plan for every task.
- Official thread tools remain the first source for user turns. agtlog 0.4.2 adds bounded offline keyword search; observed incomplete and unaddressable sessions are documented in local-history.md.

These ideas were integrated into the existing owner-specific skill, rather than importing the upstream Claude workflow. Delegated maintenance of personal context remains governed by the owner's current instructions.
