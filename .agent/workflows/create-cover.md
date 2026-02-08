---
description: Generate a book cover concept.
---
1.  **Ask User:** "Describe the scene, mood, and genre for the book cover."
2.  **Define Variables:**
    -   `Prompt`: User input.
    -   `StyleGuide`: Read `00_Story_Bible/style_guide.md` for tone.
3.  **Action:** Use `generate_image` tool.
    -   **Prompt:** Combine `Prompt` with "Book cover design, high resolution, cinematic lighting, text placeholder for title and author name" and relevant style keywords (e.g., "Sci-fi", "Fantasy", "Minimalist").
    -   **ImageName:** `book_cover_concept`
4.  **Notify:** "Cover concept generated. Check your artifacts."
