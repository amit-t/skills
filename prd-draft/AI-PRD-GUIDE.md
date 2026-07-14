# AI Feature PRDs — Full Guide

Disclosed reference for [`SKILL.md`](SKILL.md) — the complete AI PRD reference (constraints, edge cases, evaluation plan, 10 principles, template addition). Reached from the AI Behavior Contract step when drafting a PRD for an AI-powered feature.

**When to use:** When building any AI-powered feature, LLM integration, or ML product.

## Why AI PRDs Are Different

AI is fundamentally different from traditional features:
- **Non-deterministic:** Same input → different outputs
- **Probabilistic:** Can't guarantee 100% accuracy
- **Context-dependent:** Quality depends on prompt, data, user intent
- **Edge cases everywhere:** Infinite ways to break it

## AI PRD Additional Sections

### Behavior Specification (Required for AI)

Create a table with three categories:

| User Input | Expected Behavior | Category |
|------------|-------------------|----------|
| [Example 1] | [What AI should do] | ✅ Good |
| [Example 2] | [What AI should do] | ✅ Good |
| [Example 3] | [Graceful handling] | ❌ Bad |
| [Example 4] | [Must refuse] | 🚫 Reject |

**Good:** AI performs correctly
**Bad:** AI should handle gracefully (don't break)
**Reject:** AI must refuse (safety, policy violations)

**Tip:** Write 10-20 examples covering edge cases.

### AI Constraints

**Model constraints:**
- Model type: (GPT-5.2, Claude Opus 4.5, etc.)
- Max tokens: input/output limits
- Latency requirements: response time SLA
- Cost constraints: $ per 1M tokens

**Quality constraints:**
- Accuracy target: % correct responses
- Hallucination rate: max % of made-up facts
- Refusal rate: % of "I don't know" responses

**Safety constraints:**
- Content filtering requirements
- PII handling policy
- Bias mitigation requirements

### Edge Case Handling

**Common AI edge cases:**

1. **Ambiguous input**
   - AI asks clarifying questions

2. **Out-of-scope request**
   - AI explains what it can help with instead

3. **Harmful/unsafe request**
   - AI refuses with explanation

4. **Insufficient context**
   - AI asks for more information

5. **Low confidence**
   - AI admits uncertainty

### Graceful Degradation

**Fallback hierarchy:**
1. Retry with modified prompt
2. Offer alternative action
3. Escalate to human
4. Fail gracefully with clear message

### AI Evaluation Plan

**Pre-launch:**
- Test set: 100-500 hand-labeled examples
- Human evaluation: Team rates 50 outputs
- Edge case coverage: Test all known failure modes

**Post-launch:**
- Thumbs up/down feedback
- Correction rate (% of edited outputs)
- Abandonment rate
- Escalation rate

## 10 Principles for AI Products

1. **Focus on user value** - Users care about outcomes, not technology
2. **Anticipate mistakes** - Show confidence, allow corrections
3. **Start simple** - One use case, nail it, expand
4. **Make AI transparent** - What it can/can't do, when uncertain
5. **Build for iteration** - Feedback loops from Day 1
6. **Design for diverse users** - Beginners and experts
7. **Control context** - System instructions, user history, RAG
8. **Optimize for latency** - Streaming, perceived performance
9. **Safety is non-negotiable** - Input/output filtering, rate limiting
10. **Measure what matters** - Satisfaction, completion, corrections

## AI PRD Template Addition

Add this to the standard PRD for AI features:

```markdown
## AI Behavior Specification

| User Input | Expected Behavior | Category |
|------------|-------------------|----------|
| [Example] | [Response] | ✅ Good |
| [Example] | [Response] | ❌ Bad |
| [Example] | [Response] | 🚫 Reject |

## AI Constraints
- Model: [GPT-5.2 / Claude Opus 4.5 / etc.]
- Latency: P95 < ___ ms
- Accuracy target: >___%
- Hallucination rate: <___%

## Safety & Compliance
- Content filtering: [policy]
- PII handling: [policy]
- Audit logging: [policy]

## Graceful Degradation
1. [First fallback]
2. [Second fallback]
3. [Human escalation]
4. [Final error state]

## AI-Specific Kill Criteria
- Accuracy < ___% after 2 weeks
- User satisfaction < ___%
- Escalation rate > ___%
```
