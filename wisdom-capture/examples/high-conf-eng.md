# Fixture: high-confidence engineering snippet

## Input

```
Premature optimization is the root of all evil.
— Donald Knuth, https://en.wikipedia.org/wiki/Donald_Knuth
```

## Expected categorization output

```json
{
  "primary": "engineering",
  "confidence": "high",
  "tags": ["optimization", "principles"],
  "reason": "Classic engineering aphorism about code optimization.",
  "new_bucket_proposal": null,
  "second_best": "craft"
}
```
