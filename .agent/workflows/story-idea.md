---
description: Generate a story premise based on user input, informed by a cynical market analysis.
---
1.  **Enforce Market Analysis:** Check if `00_Story_Bible/market_analysis.md` exists. If not, trigger `/market-brainstorm` first to compile the cynical trend audit.
2.  **Ask User:** "What is your working title, genre, tropes, or initial character ideas?"
3.  **Read Planning Context:**
    -   `00_Story_Bible/market_analysis.md`
    -   `00_Story_Bible/style_guide.md`
    -   `00_Story_Bible/rules/FOOLSCAP_RULES.md`
    -   `00_Story_Bible/rules/TENACIOUS_RULES.md`
4.  **Action:** Generate a highly structured, genre-specific premise in `01_Planning/premise.md` using the **Architect** persona.
    -   **Requirement:** The premise must explicitly align with the commercial gaps, tropes, and hooks outlined in `market_analysis.md`.
    -   **Include:** Working Title, Genre/Sub-genres, Logline, Target Audience, Core Character Profiles (Flawed Belief vs. Healed Belief), and a brainstormed controlling idea.
5.  **Notify:** "Premise created at `01_Planning/premise.md` aligned with your cynical market analysis. You are now ready to run `/story-outline` to trigger the Phase 1 Foundation Loop."
