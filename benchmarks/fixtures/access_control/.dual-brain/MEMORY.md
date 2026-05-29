# Project Memory

## Active Constraints

- The supported elevated ownership role is `owner`.
- Keep existing admin/editor/viewer route behavior backward-compatible.

## Architecture Decisions

## Vocabulary

- "Policy" means a central authorization decision, not an inline route check.

## Rejected Alternatives

- The legacy `superuser` role is stale and must not be reintroduced.
- Inline owner checks were rejected because they scattered authorization logic.

## Open Questions

- Audit logging is out of scope for this benchmark.

## Recent Changes

## Archived Decisions
