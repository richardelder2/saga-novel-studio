---
description: Generate a chapter outline from the premise, enforced by the Foundation Score Gate.
---
1.  **Read Planning Context:**
    -   `01_Planning/premise.md`
    -   `00_Story_Bible/rules/FOOLSCAP_RULES.md`
    -   `00_Story_Bible/rules/TENACIOUS_RULES.md`
    -   `.agent/architect_instructions.md`
    -   `.agent/evaluator_instructions.md`
2.  **Action (Loop Start):** Act as the **Architect**. Create/refine the chapter outline in `01_Planning/outline.md` aligning with the 6-Beat Arc of Change, obligatory genre scenes, and target pacing.
3.  **Evaluate:** Act as the **Evaluator**. Score the outline against character-driven internal logic, pacing, and genre parameters. Save the scorecard to `01_Planning/foundation_critique.md`.
4.  **Score Gate Check:**
    -   Is the `Foundation_Score` >= 7.5?
    -   **If YES:** Proceed to step 6.
    -   **If NO:** Present the scorecard and structural gaps to the user, asking:
        -   *"Option A: Let the Architect automatically re-align the outline to fix these gaps (will loop)."*
        -   *"Option B: Force Pass (Bypass this score gate and keep my current outline)."*
5.  **User Choice Execution:**
    -   If user chooses **Option A**: Loop back to Step 2 to refine the outline based on the critic feedback in `foundation_critique.md`.
    -   If user chooses **Option B**: Proceed to step 6.
6.  **Action:** Update the local manifest and extract canon rules.
    -   **Command:** `python .agent/scripts/manage_manifest.py update --foundation-score {Foundation_Score} --phase "Phase 2: Drafting"`
    -   **Action:** Extract canon settings, characters, and rules, compiling a `00_Story_Bible/bible_canon_rules.json` file to serve as a lockable lore reference for future loops.
7.  **Notify:** "Phase 1 Foundation Loop completed! Chapter-by-chapter outline locked in `01_Planning/outline.md`, local project manifest advanced to Drafting Phase, and systemic lore rules compiled at `00_Story_Bible/bible_canon_rules.json`."

