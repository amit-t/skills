# Rubric — Stage 2: Procedure Identification

## The five questions (verbatim, spec A4 Stage 2)

1. Did this session involve a task that required a multi-step approach?
2. Was that approach non-standard — did the agent make decisions that weren't explicitly instructed?
3. Did the approach produce a notably good result?
4. Is the task type likely to recur?
5. Could the steps be generalized to similar tasks?

If the answer to **most** of these is yes, the session is flagged as containing a candidate procedure.

## 0–2 anchor table (spec C5 Stage 2)

| # | Question (from article) | 0 | 1 | 2 |
|---|---|---|---|---|
| Q1 | Did this session involve a task that required a multi-step approach? | single step | 2–3 steps | 4+ ordered steps |
| Q2 | Was the approach non-standard — did the agent make decisions that weren't explicitly instructed? | followed instructions only | some uninstructed choices | clearly discovered/adapted method |
| Q3 | Did the approach produce a notably good result? | unclear/poor | completed | completed well with positive signal |
| Q4 | Is the task type likely to recur? | one-off | plausible | already seen elsewhere |
| Q5 | Could the steps be generalized to similar tasks? | context-locked | partly | cleanly generalizable |

## Flag rule

flag if ≥3 of 5 questions score 2 AND total ≥ 7/10 AND Q2 ≥ 1; Q2 = 0 never flags.
