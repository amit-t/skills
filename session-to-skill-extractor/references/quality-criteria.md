# Quality Criteria — Spec A5

Extracting too aggressively creates a cluttered library that is harder to maintain and harder for agents to navigate. Good candidates share all five of the following. Use this as a yes/no checklist before articulating a candidate.

- [ ] **Recurrence (3+ sessions)** — the same task type seen in three or more sessions; one-off procedures rarely justify the overhead.
- [ ] **Non-obviousness** — if the agent should already know it from base instructions, capturing it adds no value; look for discovered approaches: adaptations, workarounds, multi-step methods not documented anywhere.
- [ ] **Replicability** — works reliably across instances of the same task type; highly context-specific approaches unlikely to generalize are not candidates.
- [ ] **Measurable quality** — some signal the procedure produced a good outcome: not just that it completed, but that it completed well.
- [ ] **Clarity of articulation** — if the procedure is too complex or context-dependent to write down clearly, it is not ready to be a skill; forcing unclear procedures into the library creates more problems than it solves.
