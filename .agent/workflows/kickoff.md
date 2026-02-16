---
description: Interactive "First Day" interview to populate the Story Bible.
---
1.  **Read:** `.agent/orchestrator_instructions.md` (Set the persona).
2.  **Ask User:** "Welcome to the **Novel Factory**! 📚 I'm your Orchestrator. How do you want to start today?
    
    1.  🧠 **The Brain Dump:** Paste your messy notes, snippets, and questions. I'll sort them out.
    2.  🦁 **The Tenacious Start:** Let's nail the Internal Logic (Character Truths) first.
    3.  ✨ **Brainstorming:** I have nothing. Help me generate an idea.
    
    (Reply 1, 2, or 3)"

3.  **Define Variables:**
    -   `Choice`: User input.

4.  **Branch:**
    -   **If Choice is 1 (Brain Dump):**
        1.  **Ask:** "Go ahead! Paste everything you have. I'm looking for:
            -   Story Text
            -   [Notes in brackets] for themes/structure
            -   (Parentheses) for your questions/asides"
        2.  **Action:** Analyze Input.
            -   **Drafting:** Extract narrative text to `02_Drafting/chapter_01_snippet.md`.
            -   **Premise:** Extract `[Notes]` and broad concepts to `01_Planning/premise.md`.
            -   **Questions:** Answer any `(Questions)` immediately.
        3.  **Notify:** "I've organized your notes!
            -   Snippet saved to Drafts.
            -   Premise created.
            -   *Answered your questions above.*"
            
    -   **If Choice is 2 (Tenacious):**
        1.  **Command:** Trigger `/coach-me`.
        
    -   **If Choice is 3 (Brainstorm):**
        1.  **Command:** Trigger `/story-idea`.
