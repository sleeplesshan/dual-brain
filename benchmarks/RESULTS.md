# Dual-Brain Benchmark Results

This is an early evidence snapshot from one 5-case Codex run. It is not a final scientific claim. The benchmark question is practical: does Dual-Brain spend more reasoning up front to reduce the mistakes that make a human re-prompt, repair, or re-litigate architecture?

Run source: `benchmarks/runs/20260529T013920Z`

## Human Iteration Avoidance

| Strategy | Pass rate | First-pass correctness | Human repair prompts | Trap failures | Memory regressions |
|---|---:|---:|---:|---:|---:|
| `codex_single_no_memory` | 3/5 | 1/5 | 2 | 0/2 | 2/2 |
| `codex_dual_memory` | 4/5 | 3/5 | 1 | 0/2 | 1/2 |

Dual-Brain reduced repair prompts from 2 to 1 and memory regressions from 2 to 1 in this run. That is the practical claim: spend more reasoning up front to avoid extra human correction loops later.

## Quality Summary

| Scenario | Method | Strategy | Memory | Pass | First pass | Repair loops |
|---|---|---|---:|---:|---:|---:|
| notifications | main | `codex_single_no_memory` | no | yes | yes | 0 |
| notifications | main | `codex_dual_memory` | yes | yes | yes | 0 |
| notifications | trap | `codex_single_no_memory` | no | yes | no | 1 |
| notifications | trap | `codex_dual_memory` | yes | yes | yes | 0 |
| billing | trap | `codex_single_no_memory` | no | yes | no | 1 |
| billing | trap | `codex_dual_memory` | yes | yes | no | 1 |
| notifications | memory | `codex_single_no_memory` | no | no | no | 0 |
| notifications | memory | `codex_dual_memory` | yes | yes | yes | 0 |
| access_control | memory | `codex_single_no_memory` | no | no | no | 0 |
| access_control | memory | `codex_dual_memory` | yes | no | no | 0 |

## Trap Defense

| Scenario | Single-agent | Dual-Brain |
|---|---:|---:|
| notifications | defended after 1 repair | defended first-pass |
| billing | defended after 1 repair | defended after 1 repair |

Both strategies avoided the forbidden APIs in the final state. Dual-Brain improved the `notifications` trap by catching the deprecated Slack API path before a repair prompt was needed.

## Memory Persistence

| Scenario | Single-agent | Dual-Brain |
|---|---:|---:|
| notifications | failed | passed |
| access_control | failed | failed |

The `access_control/memory` miss is important. Dual-Brain remembered the central policy registry decision, but still allowed an inline owner role check in Session 3. The benchmark correctly caught that as an architecture regression.

## Cost Summary

Time and tokens are retained as overhead/cost indicators. They are not the primary score.

| Strategy | Total wall-clock | Total tokens |
|---|---:|---:|
| `codex_single_no_memory` | ~18.6 min | ~4.56M |
| `codex_dual_memory` | ~59.2 min | ~7.63M |

Dual-Brain is expected to cost more per attempt. The benchmark asks whether that cost buys fewer human correction loops, better trap defense, and less architecture regression.
