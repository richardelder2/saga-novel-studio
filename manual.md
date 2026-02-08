# User Manual: The Agentic Novelist Workspace

## 1. System Overview
This workspace is designed to be a comprehensive "command center" for novel writing, replacing complex external automation tools (like N8N) with direct, intelligent Agent workflows within your IDE.

**Core Philosophy:**
-   **Files are Truth:** Your Story Bible and Drafts are simple Markdown files.
-   **Agents are Staff:** You have specialized "departments" (Architect, Scribe, Editor) that you summon on command.
-   **Slash Commands:** Complex multi-step processes are triggered by simple commands.

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

## 4. Updates & Extensions

### The Tenacious Writing Coach (Coming Soon)
We are currently researching the "Tenacious Writing Program" to build a specialized **Coach** persona.
-   **Goal:** To focus on mindset, sustainability, and overcoming writer's block.
-   **Status:** Pending documentation ingestion. Once active, it will offer a `/coach-me` command to help you through creative slumps.

## 5. Quick Reference
| Goal | Command |
| :--- | :--- |
| **New Idea** | `/story-idea` |
| **Outline** | `/story-outline` |
| **Draft** | `/write-chapter` |
| **Critique** | `/critique-chapter` |
| **Cover Art** | `/create-cover` |
| **Compile** | `/compile-manuscript` |
