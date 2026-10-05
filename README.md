# handoff

A handoff is the unit another chat needs to continue a job. It is a paste block plus the files that chat must open. A markdown note alone is not a handoff.

- Kind: `handoff`
- Extension: `.handoff`
- MIME: `application/x-handoff`
- Version: 1
- Declaration: `handoff.kind`
- Sample: `sample.handoff` (continues Lumen from `robot_tick_8.py`)

This type is registered in the sandbox and in this repo. It is not an OS MIME registration.

## How another chat uses it

1. Open `sample.handoff` or the `.handoff` you were given.
2. Reject it unless line 1 is `# handoff v1`.
3. Read `mission`, `continue_from`, and `stop_rule`.
4. Open every path under `FILES` before writing.
5. Take `PASTE` as the exact instruction. Do not summarize it.
6. Do not claim the job continued unless the `stop_rule` test passed.

Check a file:

```
python3 parse_handoff.py sample.handoff
```

Work continues in the repo named by `RULES` `repo`. The sample points at https://github.com/fitzyracing1/lumen.
