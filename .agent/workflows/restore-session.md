---
description: Read the local manifest and catch the agent up on current draft progress, scores, and active writing goals.
---
1.  **Action:** Programmatically update the manifest with active workspace statistics.
    -   **Command:** `python .agent/scripts/manage_manifest.py update --recalculate`
2.  **Read Context Files:**
    -   `00_Story_Bible/project_manifest.json`
    -   `01_Planning/outline.md` (if exists)
3.  **Action (Briefing Alignment):** Act as the **Orchestrator**. Analyze the current state and outline:
    -   Present a premium "Active Writing Desk Briefing" summarizing the current book title, genre, phase, word counts, and scores.
    -   Identify the next logical narrative step (e.g., "Drafting Chapter 3: The Ascent" based on the outline and existing draft files).
    -   Offer a motivational micro-tip from the **Tenacious Writing Coach** to help start the writing session.
