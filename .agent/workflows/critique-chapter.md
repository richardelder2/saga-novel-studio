---
description: Critique and polish a chapter draft using the Editorial Loop.
---
1.  **Ask User:** "Which chapter do you want to critique and edit? (e.g., '1', '2')"
2.  **Define Variables:**
    -   `ChapterNum`: User input.
    -   `DraftFile`: `02_Drafting/chapter_{ChapterNum}.md`
    -   `CritiqueFile`: `03_Review/critique_{ChapterNum}.md`
    -   `PrevScore`: 0.0
    -   `CurrentScore`: 0.0
    -   `Iteration`: 1
    -   `MaxIterations`: 3
3.  **Check Draft:** Does `DraftFile` exist?
    -   If NO: **Stop** and tell user "Please draft Chapter {ChapterNum} first."
4.  **Read Context:**
    -   `00_Story_Bible/style_guide.md`
    -   `00_Story_Bible/rules/STORY_GRID_RULES.md`
    -   `00_Story_Bible/rules/ANTI-SLOP.md`
    -   `DraftFile`
    -   `.agent/deep_editor_instructions.md`
    -   `.agent/evaluator_instructions.md`
5.  **Action (Loop Start):**
    -   Act as the **Deep Editor**. Write a rigorous critique of `DraftFile` targeting Story Grid commandments, subtext, sensory details, and POV filters.
    -   Act as the **Deep Editor**. Generate a rewritten version of the scene incorporating the critique, saving it temporarily.
    -   Act as the **Evaluator**. Score the rewritten version, saving the score in `CritiqueFile` as `CurrentScore`.
6.  **Plateau Detection Gate:**
    -   Calculate `Score_Delta` = `CurrentScore` - `PrevScore`.
    -   Is `Score_Delta` < 0.1 OR `Iteration` >= `MaxIterations`?
        -   **If YES:** Save the final rewritten chapter to `DraftFile` and proceed to step 8.
        -   **If NO:**
            -   Overwrite `DraftFile` with the temporary rewritten version.
            -   Set `PrevScore` = `CurrentScore`.
            -   Increment `Iteration` by 1.
            -   Loop back to Step 5 to let the Deep Editor perform another developmental micro-rewrite on the new draft.
7.  **Supreme Human Arbiter Gate:** Present the Editorial Critique logs in `CritiqueFile`, listing the starting score, final score, and the exact developmental value improvements. Ask:
    -   *"Option A: Accept these edits and commit changes to the draft."*
    -   *"Option B: Revert these edits and keep my previous version."*
8.  **User Choice Execution:**
    -   If user chooses **Option B**: Discard the edits (recommend using IDE git discard) to revert the file.
    -   If user chooses **Option A**: Lock in the final polished draft.
9.  **Action:** Recalculate drafting stats and update the manifest.
    -   **Command:** `python .agent/scripts/manage_manifest.py update --recalculate --editorial-score {CurrentScore} --phase "Phase 3: Review"`
10. **Notify:** "Phase 3 Editorial Loop finished after {Iteration} passes. Chapter {ChapterNum} developmental edit finalized at `DraftFile`. Critique saved at `CritiqueFile`. Manifest updated."

