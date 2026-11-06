# handoff

A handoff is the unit another chat needs to continue a job. It is a paste block plus the files that chat must open. A markdown note alone is not a handoff.

- Kind: `handoff`
- Extension: `.handoff`
- MIME: `application/x-handoff`
- Versions: 1 and 2 (v2 = pinned: `repo` and `commit` required)
- Language spec: [docs/language.md](docs/language.md)
- Declaration: `handoff.kind`
- Sample: `sample.handoff` (a v2 handoff that continues Lumen from `lumen.py`)

This type is registered in the sandbox and in this repo. It is not an OS MIME registration.

## How another chat uses it

1. Open `sample.handoff` or the `.handoff` you were given.
2. Reject it unless line 1 is `# handoff v1` or `# handoff v2`.
3. Read `mission`, `continue_from`, and `stop_rule`, plus `repo` and `commit` if set.
4. Open every path under `FILES` at `commit` in `repo` before writing.
5. Take `PASTE` as the exact instruction. Do not summarize it.
6. Do not claim the job continued unless the `stop_rule` test passed.

Check a file:

```
python3 parse_handoff.py sample.handoff
```

Work continues in the repo named by the fenced `repo` field, pinned to the `commit` field. Both are optional in v1 and required in v2. Write new handoffs as v2. The sample points at https://github.com/fitzyracing1/lumen at commit `b93be5644b6e5659606bfede4bd086d94cd215c2`.

Run the tests:

```
python3 -m unittest discover -s tests -v
```

`parse_handoff.py` checks structure only. Checking that FILES exist and running the stop_rule belong to [handoff-mcp](https://github.com/fitzyracing1/handoff-mcp).

License: MIT, see [LICENSE](LICENSE).

## Documentation

- In-repo docs: [docs/](docs/index.md)
- Wiki: [https://github.com/fitzyracing1/handoff/wiki](https://github.com/fitzyracing1/handoff/wiki)

## Plans

This project is free, and its license stays as is. Support it through [GitHub Sponsors](https://github.com/sponsors/fitzyracing1):

- **Free**: use the code, community support.
- **Pro ($49/month)**: priority issues and support.
- **Team ($199/month)**: priority support for your team plus early access.
