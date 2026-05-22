---
description: Start a new book project by cloning this workspace.
---
1.  **Ask User:** "What do you want to name your new book? (Reply with a name, or say 'generate' to get a cool one)"
2.  **Define Variables:**
    -   `UserInput`: User's reply.
3.  **Action:** Run the generator script.
    -   If `UserInput` contains "generate" or is empty:
        -   **Command:** `python start_new_book.py --generate`
    -   Else:
        -   **Command:** `python start_new_book.py --name "{UserInput}"`
4.  **Notify:** "New workspace created! Open the folder to start writing."
