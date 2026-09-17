# Anti-Patterns — Spec A7

Five common mistakes, as do-not rules. Guard against all five on every extraction run.

1. **Do not extract too broadly.** Capturing everything potentially useful yields dozens of low-quality entries that confuse agents. Apply strict quality criteria from the start.
2. **Do not skip deduplication.** Skipping it produces multiple slightly different versions of the same skill; agents presented with ambiguous choices default to general behavior, defeating the purpose.
3. **Do not write vague skill definitions.** "When asked about X, provide a thorough and helpful response" is not a skill. A skill describes specific actions, in sequence, with conditions.
4. **Do not skip closing the feedback loop.** Extraction without measurement is guesswork. Skills that don't improve outcomes shouldn't stay.
5. **Do not treat extraction as a one-time project.** It is most valuable as an ongoing process; agent behavior improves incrementally, not in a single batch.

## Vague-phrase blacklist

- "be thorough"
- "provide a helpful response"
- "use best judgment"
- "as appropriate"
- "handle accordingly"
- "search the web and then summarize"
- "when asked about X, provide a thorough and helpful response"
- "carefully"
- "properly"
- "make sure it works"
