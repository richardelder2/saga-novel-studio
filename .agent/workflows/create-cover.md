---
description: Generate a book cover concept using Google Imagen 3.0.
---
1.  **Read Context:**
    -   `00_Story_Bible/project_manifest.json`
    -   `00_Story_Bible/style_guide.md`
    -   `.env`
2.  **Ask User:** "Describe any specific visual details or art direction for the book cover (or press Enter to automatically generate based on your outline and style guide)."
3.  **Define Variables:**
    -   `VisualDetails`: User input.
4.  **Action:** Run Python cover generation script.
    -   If `VisualDetails` is empty or just whitespace:
        -   **Command:** `python .agent/scripts/generate_cover_api.py`
    -   Else:
        -   **Command:** `python .agent/scripts/generate_cover_api.py --prompt "{VisualDetails}"`
5.  **Notify:** "Book cover concept generated successfully! View the result at `04_Publishing/covers/cover_concept.png`."
