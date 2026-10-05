# handoff

Kind: handoff. Extension: `.handoff`. MIME: `application/x-handoff`. Version: 1.

A handoff is a paste block plus the files another chat must open. A markdown note alone is not one.

Line 1 is `# handoff v1`. Then a fenced block with mission, continue_from, and stop_rule. Then FILES, PASTE, and RULES.

The sample is `sample.handoff`. It continues Lumen from `robot_tick_8.py`. The declaration is `handoff.kind`. This type is registered in the sandbox and in this repo. It is not an OS MIME registration.
