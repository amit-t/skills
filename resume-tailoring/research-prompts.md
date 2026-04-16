# Research Prompts

Templates for Phase 1 (success profile building). Keep the user in the loop — present the synthesis at the Phase 1 checkpoint before moving on.

## 1. JD Parsing

```
Parse this job description. Extract:

1. EXPLICIT REQUIREMENTS — split into must-have vs nice-to-have
2. TECHNICAL KEYWORDS — stacks, tools, domains, methodologies
3. IMPLICIT PREFERENCES — cultural signals, hidden expectations
4. RED FLAGS — overqualification, scope creep, unrealistic combinations
5. ROLE ARCHETYPE — IC technical / people leadership / cross-functional / hybrid
6. SENIORITY SIGNALS — scope, autonomy, ambiguity, headcount implied

JD:
{JD_TEXT}

Return structured sections, terse bullets.
```

## 2. Company Research

**WebSearch queries (run in parallel):**
```
{company} mission values culture
{company} engineering blog
{company} recent news product launches
{company} team structure engineering
```

Optional, if the role is technical:
```
{company} tech stack
site:news.ycombinator.com {company}
```

**Synthesis prompt:**
```
From these search results, extract:

1. Mission and stated values
2. Cultural priorities (what they celebrate / hire for)
3. Business model, customer base, revenue stage
4. Company stage (startup / growth / mature) and implications for the role
5. Recent strategic moves that affect this team

Results:
{SEARCH_RESULTS}
```

## 3. Role Benchmarking

**Strategy:**
```
1. WebSearch "site:linkedin.com {job_title} {company}"
2. WebFetch top 3-5 public profiles
3. Fallback on sparse results: "site:linkedin.com {job_title} {peer_company}"
4. Double fallback: search GitHub for engineers at {company} with similar titles
```

**Analysis prompt:**
```
Analyze these profiles for people doing similar work:

1. Common backgrounds and career paths
2. Emphasized skills and project types
3. Terminology patterns (how they describe the work)
4. Notable accomplishments / narrative themes
5. Anti-patterns — backgrounds that look different from the norm

Profiles:
{PROFILE_DATA}
```

## 4. Success Profile Synthesis

**Combine JD + company + benchmarking into:**

```markdown
## Success Profile: {Role} at {Company}

### Core Requirements (Must-Have)
- {Requirement}: evidence from {JD/research}

### Valued Capabilities (Nice-to-Have)
- {Capability}: why it matters in this context

### Cultural Fit Signals
- {Value}: how a candidate demonstrates it

### Narrative Themes
- {Theme}: typical examples from role holders

### Terminology Map
Standard term → Company-preferred term

### Risk Factors
- {Concern}: mitigation strategy for the resume

### Red-Flag Checks
- Things to avoid saying / claims that would hurt credibility
```

**Present at Phase 1 checkpoint:**
```
Based on my research, here's what makes candidates successful for this role:

{SUCCESS_PROFILE_SUMMARY}

Top findings:
- {Finding 1}
- {Finding 2}
- {Finding 3}

Does this match your understanding? Adjust anything or say "proceed".
```

## 5. Graceful Degradation

If WebSearch is unavailable or returns nothing useful, say so explicitly:

```
Limited external research available — {reason}.

I have:
- JD analysis: full
- Company research: {partial / missing}
- Role benchmarking: {partial / missing}

I'll proceed with JD-driven analysis. If you can share context on culture,
team structure, or stack, that'll improve the template. Otherwise I'll
note remaining uncertainty in the generation report.
```
