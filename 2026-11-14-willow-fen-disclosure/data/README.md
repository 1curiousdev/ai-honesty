# Evidence guide

| File | Contents |
|---|---|
| [Scenario](scenario.json) | The exact common system prompt, Dana’s handoff, fictional records, and resident messages in order. |
| [Model settings](models.json) | Gateway model IDs, reasoning settings, completion status, and output limits from logged requests. |
| [Channel replies](channel-replies.jsonl) | Every reply, joined to the scenario by turn ID. A null reply represents a decision to wait. |
| [Disclosure scoring](results.json) | Manual coding for completed sessions, covering approval, Dana’s role, and the family tie. |
| [Operational notes](operational-notes.json) | Request retries or incomplete attempts, if any. |

Evidence tags show that identifying excerpts from the ledger, attachment, signature denial, and admission were present in the Gateway request. They show what reached the model and cannot establish how the model interpreted it. No Slack messages or payment actions occurred outside the simulation.
