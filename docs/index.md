# handoff

A `.handoff` file (kind `handoff`, version 1, MIME `application/x-handoff`) carries what another chat needs to continue a job: a paste block plus the files it must open. The type is declared in `handoff.kind` and is not an OS MIME registration.

| File | Content |
|---|---|
| `handoff.kind` | spec: structure, parse rules, write rules |
| `sample.handoff` | example that continues Lumen from `robot_tick_8.py` |
| `parse_handoff.py` | standard-library Python validator and summary printer |
| `handoff-README.md` | short description |

## Format (from `handoff.kind`)

1. Line 1 is `# handoff v1`.
2. A `---` fenced block with `mission`, `continue_from`, and `stop_rule`.
3. `FILES` (one path per line), `PASTE` (verbatim text), and `RULES` (`KEY: value`).

A handoff with an empty `FILES` or `PASTE` section is invalid.

## Getting started

```
python3 parse_handoff.py sample.handoff
```

It prints the mission, continue_from, stop_rule, the file list, the paste length, and the rule count. If the file is invalid it prints `INVALID: <reason>` to stderr and exits with code 1. With no argument it reads `sample.handoff`.

## Using a handoff in another chat

Reject the file unless line 1 is `# handoff v1`. Open every path under `FILES` before writing anything, and treat `PASTE` as the exact instruction. Do not claim the job continued unless the `stop_rule` test passed.

Copyright (c) 2026 Joshua Almeida
