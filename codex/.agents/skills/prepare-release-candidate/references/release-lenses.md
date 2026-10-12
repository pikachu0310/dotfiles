# Release lenses

Select the checks that match the release. Do not expand a small release into a universal compliance audit.

## Promise and first value

- Public name, description, screenshots, pricing, compatibility, and announcement claims match the candidate.
- A new user can understand the value, start safely, and reach the first successful outcome.
- The returning-user path preserves state and does not replay onboarding destructively.
- Documentation and support routes explain the most likely point of failure.

## Functional integrity

- Primary and secondary journeys complete end to end.
- Empty, loading, partial-data, rate-limited, offline, expired-session, and dependency-failure states recover safely.
- Links, downloads, routes, deep links, assets, and version identifiers resolve correctly.
- Mobile, desktop, browser, VR, controller, or multiplayer behavior matches the declared support boundary.

## Data, security, and trust

- Authentication and authorization deny cross-user access and unintended writes.
- Server-authoritative or trusted-side validation covers important rewards, purchases, scores, and state changes.
- Input, upload, URL, and remote-call boundaries validate type, size, rate, and ownership.
- Privacy, public visibility, unofficial status, data collection, deletion, and irreversible actions are explained where needed.
- Secrets and personal data do not appear in code, logs, screenshots, artifacts, or reports.

## Operations and recovery

- Capacity, quotas, rate limits, external dependencies, monitoring, alerting, and expected load are understood.
- Migration, backup, restore, rollback, and forward-fix paths are feasible and do not rely on untested assumptions.
- Logs identify failure without exposing secrets; operators can distinguish user error from service failure.
- The release artifact is reproducible from an identified revision and configuration.

## Experience quality

- The first screen or first moments communicate purpose and next action.
- Important controls are legible, reachable, and provide immediate feedback.
- Accessibility, reduced motion, contrast, keyboard/focus, readable error text, and zoom are checked where applicable.
- Performance is measured on the core path: load time, response time, frame rate, memory, package size, or server capacity as relevant.
- Visual and audio assets are licensed, attributed, and appropriate for the release destination.

## Human launch check

Keep the final manual check short enough that a person will actually perform it. Prefer five high-signal checks tied to the riskiest unautomated assumptions: correct account and destination, production configuration, first live transaction or session, monitoring visibility, and rollback readiness.
