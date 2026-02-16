---
description: Generate a book cover concept.
---
1.  **Ask User:** "Describe the scene, mood, and genre for the book cover."
2.  **Define Variables:**
    -   `Prompt`: User input.
    -   `StyleGuide`: Read `00_Story_Bible/style_guide.md` for tone.
    -   `ReferenceDir`: `04_Publishing/cover_references/`
3.  **Check:** Are there files in `ReferenceDir`?
    -   If YES: Use them as `ImagePaths`.
    -   If NO: Generate from scratch.
4.  **Action:** Use `generate_image` tool.
    -   **Prompt:** Combine `Prompt` with "Book cover design, high resolution, cinematic lighting, text placeholder for title and author name" and relevant style keywords (e.g., "Sci-fi", "Fantasy", "Minimalist").
    -   **ImagePaths:** (Optional, from Step 3).
    -   **ImageName:** `book_cover_concept`
5.  **Notify:** "Cover concept generated based on your prompt (and references if provided). Check your artifacts."
