# Novel Writing Workspace (Agent Edition)

Welcome to your AI-powered writing studio. This workspace is designed to replicate the "Nerdy Novelist" workflows directly in your IDE, using me (the AI Agent) as your collaborator.

## Automation (Slash Commands)

This workspace is equipped with **Slash Commands** to automate your process.

1.  **Idea Generation**:
    -   Run `/story-idea` to brainstorm and create your premise.
2.  **Outlining**:
    -   Run `/story-outline` to have the Architect generate a full chapter outline.
3.  **Drafting**:
    -   Run `/write-chapter` (e.g., "Chapter 1") to have the Scribe draft a scene based on your beats.
4.  **Critique**:
    -   Run `/critique-chapter` to get a Deep Editor review.
5.  **Publishing**:
    -   Run `/create-cover` to generate cover art.
    -   Run `/compile-manuscript` to merge all chapters into a single file for export.

## Directory Structure

- **00_Story_Bible/**: The source of truth for your story world.
    - `characters/`: One Markdown file per character.
    - `locations/`: Setting descriptions.
    - `lore/`: Magic systems, history, technology.
    - `style_guide.md`: Your voice, tone, and formatting rules.
- **01_Planning/**: Where the story takes shape.
    - `premise.md`: The "elevator pitch" or brain dump of your idea.
    - `outline.md`: High-level chapter summaries.
    - `beats/`: Detailed beat sheets for every scene (e.g., `chapter_01_beats.md`).
- **02_Drafting/**: The manuscript itself.
- **03_Review/**: Editor notes and alternate drafts.
- **04_Publishing/**: Generated covers and final exports.
- **.agent/**: System instructions and workflows.

## Getting Started

1.  Open `00_Story_Bible/style_guide.md` and fill in your preferences.
2.  Run `/story-idea` to start brainstorming!
