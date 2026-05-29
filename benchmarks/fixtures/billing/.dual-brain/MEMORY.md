# Project Memory

## Active Constraints

- Invoice totals must round to cents using half-up decimal rounding.
- Preserve `calculate_invoice_total(...)` for existing callers.

## Architecture Decisions

## Vocabulary

- "Money" means an explicit value object backed by `Decimal`, not raw floats.

## Rejected Alternatives

- `Money.round_bankers()` does not exist and contradicts the half-up rounding rule.
- Plain float totals were rejected because rounding drift broke regional tax calculations.

## Open Questions

- Coupon validation can stay out of scope; this benchmark only needs deterministic coupon application.

## Recent Changes

## Archived Decisions
