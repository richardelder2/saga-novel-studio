---
description: Draft a chapter based on its beat sheet.
---
1.  **Ask User:** "Which chapter do you want to write? (e.g., '1', '2')"
2.  **Define Variables:**
    -   `ChapterNum`: User input.
    -   `BeatFile`: `01_Planning/beats/chapter_{ChapterNum}_beats.md`
    -   `DraftFile`: `02_Drafting/chapter_{ChapterNum}.md`
3.  **Check:** Does `BeatFile` exist?
    -   If NO: **Stop** and tell user "Please create the beat sheet for Chapter {ChapterNum} first."
4.  **Read:**
    -   `00_Story_Bible/style_guide.md`
    -   `00_Story_Bible/characters/` (Read all character files for context).
    -   `BeatFile`
    -   `.agent/scribe_instructions.md` (or `.agent/sensory_drafter_instructions.md` if user prefers).
5.  **Action:** Act as the **Scribe**. Write the chapter prose in `DraftFile`.
6.  **Notify:** "Chapter {ChapterNum} drafted at `DraftFile`."
