# The handoff language

This document is the source of truth for the `.handoff` language. `handoff.kind` is the short declaration and must agree with it. `parse_handoff.py` is the reference implementation. The runtime ([handoff-mcp](https://github.com/fitzyracing1/handoff-mcp)) opens files, checks they exist, and runs the stop test; the language only defines what a well-formed handoff says.

## 1. Purpose

A handoff is the unit another chat needs to continue a job: the exact instruction (PASTE), the files it must open (FILES), where those files live (repo at commit), and the test that decides whether the job continued (stop_rule). A summary or a note without files is not a handoff.

## 2. Versions

| Banner | repo | commit |
|---|---|---|
| `# handoff v1` | optional | optional |
| `# handoff v2` | required | required |

v2 is a *pinned* handoff. Every v1 rule applies to v2. Any valid v2 document with its banner changed to v1 is a valid v1 document. A reader must reject any other banner.

## 3. Grammar

```
handoff   = banner NL fence NL meta* fence NL section*
banner    = "# handoff v1" | "# handoff v2"
fence     = "---"
meta      = key ":" value NL          ; split on the first ":", both sides trimmed
section   = files | paste | rules     ; any order, each heading on its own line
files     = "FILES" NL (path NL | blank NL)*
paste     = "PASTE" NL (line NL)*
rules     = "RULES" NL (rule NL | blank NL)*
rule      = key ": " value            ; split on the first ": "
```

- A section heading is a line that is exactly `FILES`, `PASTE`, or `RULES`. Everything up to the next heading belongs to that section.
- Lines after the closing fence and before the first heading are ignored.
- Meta lines that are blank or contain no `:` are ignored. Unknown meta keys are allowed and ignored.

## 4. Fields

| Field | Where | Meaning |
|---|---|---|
| `mission` | meta, required | What the job is, in one line. Name the body to continue, not a summary of what happened. |
| `continue_from` | meta, required | The file or point the next chat builds on. |
| `stop_rule` | meta, required | The test that decides whether the job continued. |
| `repo` | meta, v1 optional / v2 required | `http://` or `https://` URL of the repository the work continues in. |
| `commit` | meta, v1 optional / v2 required | Git SHA, 7 to 40 lowercase hex characters, that FILES are read at. Requires `repo`. |
| `FILES` | section, required | Paths, one per line, relative to the root of `repo` at `commit`. Blank lines ignored. |
| `PASTE` | section, required | The exact text the next chat must receive. Verbatim. |
| `RULES` | section, optional | `KEY: value` pairs that carry extra constraints. |

## 5. Well-formedness

A document is well formed only if all of these hold:

1. Line 1 is a known banner.
2. Line 2 is `---` and a later line closes the fence with `---`.
3. `mission`, `continue_from`, and `stop_rule` are present and non-empty.
4. If present, `repo` is an http(s) URL with no whitespace, and `commit` matches `[0-9a-f]{7,40}`.
5. `commit` is not present without `repo`.
6. In v2, `repo` and `commit` are present.
7. FILES has at least one non-blank path.
8. PASTE has non-whitespace text.
9. Every non-blank RULES line contains `: `.

A reader that finds a violation must reject the whole document. The reference parser prints `INVALID: <reason>` and exits 1.

## 6. Meaning

- **PASTE is verbatim.** The next chat receives it exactly. It must not be summarized, reworded, or merged with other text.
- **FILES are paths in `repo` at `commit`.** The next chat opens every listed path at that commit before writing. Without a pin (v1), the version is whatever the reader has, which is why v2 exists.
- **The stop rule binds the claim.** Nobody may claim the job continued unless the `stop_rule` test passed. The language defines this obligation; running the test is the runtime's job.
- Writers list only files the next chat must open.

## 7. What the language does not check

Well-formedness is local and offline. Whether FILES exist at `commit`, whether `repo` is reachable, and whether `stop_rule` passes are runtime checks (handoff-mcp).

## 8. Versioning

- The banner names the version. Readers reject banners they do not know.
- A new version may add requirements or fields. It must not change the meaning of an existing field.
- v1 documents stay valid forever. New handoffs should be written as v2.

## Example

`sample.handoff` is a valid v2 document that continues Lumen at a pinned commit.
