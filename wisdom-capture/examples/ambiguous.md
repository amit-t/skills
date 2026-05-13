# Fixture: ambiguous between writing + leadership

## Input

```
Write drunk, edit sober. The first draft of anything is shit. — apocryphal,
sometimes attributed to Hemingway. Useful for any one-pager, memo, or strategy
doc. If you can't ship the first draft, you can't ship at all.
```

## Expected categorization output

```json
{
  "primary": "writing",
  "confidence": "med",
  "tags": ["drafting", "shipping", "iteration"],
  "reason": "Primarily a writing-craft aphorism with a leadership/decision-making secondary read.",
  "new_bucket_proposal": null,
  "second_best": "leadership"
}
```
