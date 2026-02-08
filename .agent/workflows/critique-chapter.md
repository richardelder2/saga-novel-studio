---
description: Critique a chapter draft using the Deep Editor persona.
---
1.  **Ask User:** "Which chapter do you want to critique? (e.g., '1', '2')"
2.  **Define Variables:**
    -   `ChapterNum`: User input.
    -   `DraftFile`: `02_Drafting/chapter_{ChapterNum}.md`
    -   `CritiqueFile`: `03_Review/critique_{ChapterNum}.md`
3.  **Check:** Does `DraftFile` exist?
    -   If NO: **Stop** and tell user "Please draft Chapter {ChapterNum} first."
4.  **Read:**
    -   `00_Story_Bible/style_guide.md`
    -   `DraftFile`
    -   `.agent/deep_editor_instructions.md`
5.  **Action:** Act as the **Deep Editor**. Provide a critique of `DraftFile` focusing on Pacing, POV, and Show/Don't Tell. Save the critique and a rewritten version of the scene to `CritiqueFile`.
6.  **Notify:** "Critique for Chapter {ChapterNum} saved to `CritiqueFile`."
