# User Manual: The Agentic Novelist Workspace

## 1. System Overview
This workspace is designed to be a comprehensive "command center" for novel writing, replacing complex external automation tools (like N8N) with direct, intelligent Agent workflows within your IDE.

**Core Philosophy:**
-   **Files are Truth:** Your Story Bible and Drafts are simple Markdown files.
-   **Agents are Staff:** You have specialized "departments" (Architect, Scribe, Editor) that you summon on command.
-   **Slash Commands:** Complex multi-step processes are triggered by simple commands.

### 1.1 Project Structure Strategy
**Recommendation: One Workspace = One Book.**

### 1.1 Project Structure Strategy
**Recommendation: One Workspace = One Book.**

### 1.1 Project Structure Strategy
**Recommendation: One Workspace = One Book.**

**How to start a new book:**
1.  **Command:** `/start-new-book`
    -   The Agent will generate a cool name and create a new folder for you.
2.  **Open the new folder.**
3.  **Command:** `/kickoff`
    -   **The Orchestrator** will greet you and offer a menu:
        -   🧠 **Brain Dump:** Paste your messy notes, snippets, and questions. I'll sort them out.
        -   🦁 **Tenacious Start:** Jump straight to the Internal Logic.
        -   ✨ **Brainstorm:** Get help generating an idea.
    -   **Tip:** Feel free to use `[brackets]` for notes and `(parentheses)` for asides. The Orchestrator knows how to read them!

## 2. The Core Workflow Loop

The system follows a linear progression from idea to manuscript, though you can jump between stages at any time.

### Phase 1: Planning
**Objective:** Turn a spark of an idea into a solid roadmap.

1.  **Brainstorming**:
    -   **Command:** `/story-idea`
    -   **Action:** The Agent interviews you about genre and tropes, then generates a **Premise** in `01_Planning/premise.md`.
2.  **Outlining**:
    -   **Command:** `/story-outline`
    -   **Action:** The **Architect** persona reads your premise and generates a chapter-by-chapter **Outline** in `01_Planning/outline.md`.
3.  **Beats**:
    -   **Manual Step:** Create beat sheets in `01_Planning/beats/`.
    -   **Tip:** You can ask the agent: *"Act as the Architect. Create a beat sheet for Chapter 3 based on the outline."*

### Phase 2: Drafting
**Objective:** Get words on the page.

1.  **Writing**:
    -   **Command:** `/write-chapter`
    -   **Input:** You provide the Chapter Number (e.g., "1").
    -   **Action:** The **Scribe** persona reads your Beat Sheet, Style Guide, and Character Profiles, then drafts the chapter in `02_Drafting/`.

### Phase 3: Review & Refine
**Objective:** Polish the raw draft.

1.  **Critique**:
    -   **Command:** `/critique-chapter`
    -   **Action:** The **Deep Editor** persona analyzes your draft for specific issues (Pacing, POV filtering, Show-Don't-Tell) and provides a critique + rewrite in `03_Review/`.
2.  **Consistency Check**:
    -   **Command:** *"Act as the Lore Keeper. Check Chapter X against the Story Bible."*
    -   **Action:** verification of facts (eye color, magic rules, history).

### Phase 4: Publishing
**Objective:** Prepare for the world.

1.  **Cover Art**:
    -   **Command:** `/create-cover`
    -   **Action:** Generates high-quality cover art options based on your story's metadata.
2.  **Compilation**:
    -   **Command:** `/compile-manuscript`
    -   **Action:** Merges all chapters into a single `Full_Manuscript.md` file, ready for export or conversion to EPUB/PDF.

## 3. The "Staff" (Agent Personas)

These are the specialized instructions located in `.agent/`. You can edit these files to change how the agents behave!

-   **The Architect** (`architect_instructions.md`): Structural expert. Good at pacing and plot arcs.
-   **The Scribe** (`scribe_instructions.md`): Your ghostwriter. Focuses on getting the story told.
-   **The Sensory Drafter** (`sensory_drafter_instructions.md`): An alternative drafter focused on deep immersion and sensory details.
-   **The Deep Editor** (`deep_editor_instructions.md`): A ruthless critic.
-   **The Lore Keeper** (`lore_keeper_instructions.md`): Technical continuity adherence.

## 5. Updates & Extensions

### The Tenacious Writing Coach (Active)
Based on the "Novel Plotting Untangled" method by Emily & Rachel.

-   **Goal:** To align your plot with your character's internal journey.
-   **Workbook:** `01_Planning/tenacious_workbook.md` helps you map out the "Internal Logic Proof" and "Pivot Plans".
-   **Command:** `/coach-me` - The coach will review your workbook and help you untangle plot knots.

## 6. Version Control (Safety Net)

Because we are working in an IDE, we use **Git** to keep your work safe.

-   **"Save Draft" (Commit):** Whenever you hit a milestone (e.g., finishing a chapter), open the Source Control tab in your IDE and commit your changes with a message like "Finished Chapter 1 Draft".
-   **"Undo" (Revert):** If an Agent makes a mess of a rewrite, you can discard changes in the Source Control tab to revert the file to its last saved state.
-   **"Experiment" (Branch):** Want to try a new ending without losing the old one? Create a new branch (e.g., `alternate-ending`) and work there safely.

## 7. Using References

You can teach the agents your preferred style!

### Text Style References
-   **Goal:** Make the Scribe write like your favorite author (or your past work).
-   **Method 1:** Paste a text sample into `00_Story_Bible/references/sample.txt`.
-   **Method 2:** Run `/analyze-style`. I will ask you to paste the text, and I'll extract the "voice rules" into your `style_guide.md`.

### Visual References (Book Covers)
-   **Goal:** Create cover art that matches a specific vibe.
-   **Method:**
    1.  Save reference images (JPG/PNG) into `04_Publishing/cover_references/`.
    2.  Run `/create-cover`.
    3.  I will automatically use those images to guide the style of the new cover.

## 8. Quick Reference
| Goal | Command |
| :--- | :--- |
| **Start New Book** | `/start-new-book` |
| **Analyze Style** | `/analyze-style` |
| **New Idea** | `/story-idea` |
| **Outline** | `/story-outline` |
| **Draft** | `/write-chapter` |
| **Critique** | `/critique-chapter` |
| **Cover Art** | `/create-cover` |
| **Compile** | `/compile-manuscript` |
