# UX/UI Integration Rules

Disclosed reference for `/eng-spec` Step 4. Applies only when UX/UI design assets were found for the PRD code (see Context Routing); if none were found, skip this file and go straight to the SPEC skeleton in `TEMPLATES.md`.

**Before writing: cross-reference all loaded UX/UI assets.**

Use UX assets to inform these sections of the SPEC:

| UX Asset | Informs SPEC Section |
|----------|---------------------|
| **Screens** (HTML) | Section 2 (data model fields visible in forms/displays), Section 5 (API endpoints the UI calls), Section 8 (error states shown in UI) |
| **Wireframes** | Section 5 (API shape — what data the UI needs, in what structure), Section 7 (sequence flows matching interaction steps) |
| **User flows** | Section 7 (sequence diagrams — map each UI step to an API call), Section 8 (error paths shown in flow) |
| **Handoffs** | Section 3 (port interfaces — what the frontend contract requires), Section 5 (request/response shape — form fields = request body fields) |
| **Design reviews** | Section 8 (edge cases flagged in design review), Section 9 (security considerations flagged by design) |

**Specific rules when UX assets are present:**
- Every form field visible in a screen must appear as a field in the request body schema (Section 5)
- Every data element displayed in a screen must appear in the response body schema (Section 5)
- Every error message shown in a screen must appear in Section 8 with its HTTP code and error code string
- Every step in a user flow must map to at least one API call in Section 5 or a client-side operation noted as such
- If a screen shows data that spans multiple entities, the API response shape must reflect that join/aggregation

**Note screen-driven decisions in the SPEC:**
When a UX screen drives a data model or API decision, annotate it:
```
// Field required by auth-login.html — email input
email: varchar(255) NOT NULL
```
