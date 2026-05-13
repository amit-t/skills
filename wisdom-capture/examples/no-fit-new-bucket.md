# Fixture: forces a new-bucket proposal

## Input

```
The market can stay irrational longer than you can stay solvent. — Keynes.
Applies to any timing-dependent bet: shorts, market entries, layoffs timed
to a downturn.
```

## Expected categorization output

```json
{
  "primary": "life",
  "confidence": "low",
  "tags": ["timing", "markets", "risk"],
  "reason": "Concerns financial markets and timing of decisions — fits 'life' weakly. Better served by a dedicated 'investing' or 'decisions' bucket.",
  "new_bucket_proposal": {
    "key": "investing",
    "label": "Investing",
    "color": "cyan-accent",
    "reason": "Quotes about markets, capital allocation, and risk recur often enough to deserve their own bucket."
  },
  "second_best": "leadership"
}
```
