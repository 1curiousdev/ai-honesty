# Data guide

| File | Contents |
|---|---|
| [Scenarios](scenarios.json) | Exact common system prompt, handoffs, folder updates, and counterpart questions. |
| [Models](models.json) | Gateway model IDs, reasoning efforts, output limits, and whether a session was from the Terra pilot. |
| [Replies](replies.jsonl) | Visible replies keyed by model, case, and turn. Null represents silence. Evidence tags identify which record excerpts were in the Gateway request. |
| [Scoring](results.json) | Manual scoring keyed by model and case. Disclosure values give the first turn where the fact was revealed. Null indicates that the transcript did not reveal it. |
| [Operational notes](operational-notes.json) | Request retries and incomplete attempts, if any. |
