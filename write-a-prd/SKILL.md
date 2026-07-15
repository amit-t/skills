---
name: write-a-prd
description: Create a PRD through user interview, codebase exploration, and module design, then submit as a GitHub issue. Use when the user wants to write a PRD or plan a new feature.
---

You may skip steps if you don't consider them necessary.

1. Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions.

2. Explore the repo to verify their assertions and understand the current state of the codebase.

3. Interview the user relentlessly about every aspect of this plan, walking down each branch of the design tree and resolving dependencies between decisions one-by-one, until every branch is resolved and the user confirms the design.

4. Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

5. Once the user has confirmed the design (step 3) and the modules (step 4), write the PRD using the template in [`PRD-TEMPLATE.md`](PRD-TEMPLATE.md). Submit the PRD as a GitHub issue.
