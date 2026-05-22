---
description: Run the Phase 4 Production Command to compile and typeset the manuscript.
---
1.  **Ask User:** "Which format would you like to compile? (e.g., '1' for Typeset HTML/PDF, '2' for ePUB Container, '3' for Audiobook Dialogue Parser)"
2.  **Define Variables:**
    -   `FormatChoice`: User input.
3.  **Read Context:**
    -   `00_Story_Bible/style_guide.md`
    -   `00_Story_Bible/bible_canon_rules.json`
    -   `.agent/scripts/`
4.  **Execute Compiler:**
    -   **If FormatChoice is '1' (Typeset HTML/PDF):**
        -   **Action:** Run Python typesetting script.
        -   **Command:** `python .agent/scripts/typeset_book.py`
        -   **Result:** Generates a print-ready typeset HTML file at `04_Publishing/typeset_manuscript.html` using professional CSS print styling, drop caps, headers, page numbers, and custom graphic ornaments.
    -   **If FormatChoice is '2' (ePUB):**
        -   **Action:** Compile ePUB metadata.
        -   **Command:** `python .agent/scripts/compile_epub.py`
        -   **Result:** Generates a structured ePUB archive draft in `04_Publishing/`.
    -   **If FormatChoice is '3' (Audiobook Synthesizer):**
        -   **Action:** Parse all dialogue and synthesize to multi-voice speech.
        -   **Command:** `python .agent/scripts/parse_audiobook.py`
        -   **Command:** `python .agent/scripts/synthesize_audiobook.py`
        -   **Result:** Extracts dialogue into `audiobook_script.csv` and uses the Google Cloud TTS REST API to compile a high-quality multi-voice MP3 audiobook at `04_Publishing/audiobook.mp3`.
5.  **Action:** Update the local manifest state.
    -   **Command:** `python .agent/scripts/manage_manifest.py update --phase "Phase 4: Production"`
6.  **Notify:** "Phase 4 Production Command successfully run! Compiled files generated in `04_Publishing/`. Local manifest updated."

