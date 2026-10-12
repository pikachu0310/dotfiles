# Public Codex operations package

This repository contains public workflow source, not the operator's private context. Use README.md as the human entry. Keep changes scoped, preserve third-party licenses and version metadata, and keep private context, credentials, session IDs, runtime state and logs outside this repository. Public template examples do not authorize operations against a user's external accounts.

The actual environment remains separate. Do not install or alter a user's global configuration without an installation request. For this package's maintenance, group necessary checks after a substantial change; do not introduce per-edit QA loops or fixed-score rewriting.

Skills under .agents/skills are repository-local. The Intent plugin is installed through its marketplace, not copied into cache. Preserve its one-outcome/one-chat contract. Changes intended for publication need a reviewed concrete payload and current authorization; do not change a private repository's visibility.
