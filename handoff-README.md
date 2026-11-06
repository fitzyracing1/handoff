# handoff

Kind: handoff. Extension: `.handoff`. MIME: `application/x-handoff`. Versions: 1 and 2. Spec: `docs/language.md`.

A handoff is a paste block plus the files another chat must open. A markdown note alone is not one.

Line 1 is `# handoff v1` or `# handoff v2`. v2 requires repo and commit. Then a fenced block with mission, continue_from, and stop_rule, plus repo (URL) and commit (git SHA), optional in v1 and required in v2, that pin where FILES are read. Then FILES, PASTE, and RULES.

The sample is `sample.handoff`. It is a v2 handoff that continues Lumen from `lumen.py`. The declaration is `handoff.kind`. This type is registered in the sandbox and in this repo. It is not an OS MIME registration.
