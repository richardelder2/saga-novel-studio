---
description: Analyze a text sample to mimic its writing style.
---
1.  **Ask User:** "Please paste the text sample you want me to analyze (or provide the filename if it's in `00_Story_Bible/references/`)."
2.  **Define Variables:**
    -   `InputText`: User input.
    -   `StyleGuide`: `00_Story_Bible/style_guide.md`
3.  **Action:** Analyze the text.
    -   Identify: Tone, Sentence Structure (length, complexity), POV, Vocabulary level, and specific quirks.
    -   Create a summary of these "Voice Rules".
4.  **Update File:** Append these rules to `00_Story_Bible/style_guide.md` under a new header "Analyzed Style References".
5.  **Notify:** "I've updated your Style Guide with the new voice rules. I will use this usage for future drafts."
