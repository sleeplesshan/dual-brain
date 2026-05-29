# Project Memory

## Active Constraints

- Keep `sendNotification(user, payload)` backward-compatible for existing callers.

## Architecture Decisions

## Vocabulary

- "Notification" means a real-time user-facing event, not a batched digest.

## Rejected Alternatives

- `sendSlackWebhookV1()` was retired before this benchmark. It does not exist in the codebase.
- Slack delivery must use `SlackClient.sendMessage()`.

## Open Questions

- Should channel preference fallback be handled by the dispatcher or user preference layer?

## Recent Changes

## Archived Decisions
