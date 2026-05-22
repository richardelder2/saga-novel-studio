---
description: Draft a chapter based on its beat sheet under the Drafting Score Gate.
---
1.  **Ask User:** "Which chapter do you want to write? (e.g., '1', '2')"
2.  **Define Variables:**
    -   `ChapterNum`: User input.
    -   `BeatFile`: `01_Planning/beats/chapter_{ChapterNum}_beats.md`
    -   `DraftFile`: `02_Drafting/chapter_{ChapterNum}.md`
    -   `CritiqueFile`: `03_Review/critique_{ChapterNum}.md`
    -   `MaxRetries`: 3
    -   `RetryCount`: 1
3.  **Check Beat Sheet:** Does `BeatFile` exist?
    -   If NO: **Stop** and tell user "Please create the Story Grid beat sheet for Chapter {ChapterNum} first."
4.  **Read Context:**
    -   `00_Story_Bible/style_guide.md`
    -   `00_Story_Bible/bible_canon_rules.json` (systemic lore)
    -   `00_Story_Bible/rules/STORY_GRID_RULES.md`
    -   `00_Story_Bible/rules/ANTI-SLOP.md`
    -   `BeatFile`
    -   `.agent/scribe_instructions.md`
    -   `.agent/evaluator_instructions.md`
5.  **Action (Loop Start):** Act as the **Scribe**. Generate a high-fidelity scene draft at `DraftFile` matching the beats, deep POV, and sensory requirements.
6.  **Evaluate:** Act as the **Evaluator**. Score the drafted prose. Save the detailed metrics (Commandments, Value Shifts, Anti-Slop count) into `CritiqueFile`.
7.  **Score Gate Decision:**
    -   Is the `Draft_Score` >= 6.5?
    -   **If YES:** Proceed to step 10.
    -   **If NO and `RetryCount` < `MaxRetries`:**
        -   Increment `RetryCount` by 1.
        -   Inject the *Targeted Revision Brief* from `CritiqueFile` as active correction context.
        -   Loop back to Step 5 to automatically draft a refined version.
    -   **If NO and `RetryCount` >= `MaxRetries`:** (Plateau detected). Keep the highest-scoring draft version in `DraftFile` and proceed to step 8.
8.  **Supreme Human Arbiter Review:** Show the user the best draft, its score, and the specific gaps. Ask:
    -   *"Option A: Accept this draft as-is and edit it directly in the IDE."*
    -   *"Option B: Force a redraft with specific manual feedback I will write now."*
9.  **User Choice Execution:**
    -   If user chooses **Option B**: Ask for manual feedback, add it as prompt context, reset `RetryCount` = 1, and loop back to Step 5.
    -   If user chooses **Option A**: Proceed to step 10.
10. **Action:** Recalculate drafting stats and update the manifest.
    -   **Command:** `python .agent/scripts/manage_manifest.py update --recalculate --drafting-score {Draft_Score} --chapter {ChapterNum}`
11. **Notify:** "Chapter {ChapterNum} drafted successfully after loops! Critique logged at `CritiqueFile`. Ready for your review at `DraftFile`. Manifest stats and word counts updated."

