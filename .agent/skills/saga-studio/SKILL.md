---
name: saga-studio
description: Orchestrate advanced novel writing workflows (outlining, drafting, developmental edits, epub publishing, and multi-voice audiobook WAV synthesis) using the SAGA CLI.
---

# SAGA Studio Agentic Skill

This skill equips AI agents with the capabilities of the **SAGA Novel Engineering Studio**. By reading this skill, an agent learns how to coordinate story world-building, generate premises, construct beat sheets, draft chapters with self-correcting critique retries, compile eBooks, and synthesize multi-voice TTS audiobooks.

---

## 🛠️ Core Capabilities & CLI Commands

Agents should execute SAGA CLI commands or Python wrappers relative to the target project directory. SAGA automatically handles dynamic redirection to respect local project branch parameters.

### 1. Project Management & Status Checks
*   **Onboard a New Book Vault:**
    ```bash
    saga --init <folder_name>
    ```
    *(Initializes folder directories, seeds loglines, configures manifest JSON, and sets up local Git tracking).*
*   **Compile Global Registry Directory:**
    ```bash
    saga --dashboard
    ```
    *(Renders a tabular status board summarizing all registered novels, active phases, total words, critic scores, and branch details).*
*   **Query Active Project Status:**
    ```bash
    saga --status
    ```
    *(Displays the split-view dashboard, pulling environment variables, progress bars, and Quality Score Gates).*

### 2. Creative Narrative Engine
*   **Outline Beat Sheets:**
    ```bash
    saga --outline
    ```
    *(Generates a cynical market trend analysis, drafts a 6-beat chapter outline, audits structural rules, and locks in the Foundation Score).*
*   **Draft Prose Chapters:**
    ```bash
    saga --draft <chapter_number>
    ```
    *(Drafts the chapter against its beatsheet, running up to 3 self-correction retry cycles using an adversarial AI Critic until the prose scores above a 7.5 threshold. Performs a Deep Editor developmental edit, canon lore updates, and Git auto-commits).*
*   **Trigger Autonomous YOLO Loop:**
    ```bash
    saga --yolo
    ```
    *(Launches hands-free autonomous novel engineering from outlining directly through formatting and audiobook synthesis).*

### 3. Production & Publishing
*   **Compile Print Layouts & Multi-Voice Audiobooks:**
    ```bash
    saga --publish
    ```
    *(Renders print typeset HTML, compiles ePUB eBook containers, extracts speaker dialog scripts, and synthesizes multi-voice WAV audiobooks using prebuilt Gemini TTS voices).*

---

## 📑 State Schema & Directory Rules

Agents MUST read and update standard markdown assets to maintain narrative continuity:

1.  **Story Bible (`00_Story_Bible/`):**
    *   `project_manifest.json`: The core status tracking file. Contains `title`, `genre`, `status` (`active_phase`, `current_chapter`, `word_count`), and `latest_scores` (gates).
    *   `characters/`: One markdown profile per character. Voice assignments must specify a prebuilt TTS voice (e.g. `Fenrir`, `Aoede`, `Leda`, `Autonoe`).
    *   `style_guide.md`: Strict voice profiles and anti-slop rules.
2.  **Narrative Planning (`01_Planning/`):**
    *   `premise.md`: Logline and value shifts.
    *   `outline.md`: Chapter structural breakdown.
    *   `beats/`: Bullet beatsheets per chapter (e.g. `chapter_01_beats.md`).
3.  **Drafting (`02_Drafting/`):**
    *   Markdown files containing chapter prose (e.g. `chapter_01.md`).
4.  **Review Logs (`03_Review/`):**
    *   Adversarial audit critiques (`critique_01.md`).

---

## 🔧 Environment & Dependencies

This skill relies on:
- **`google-genai`:** Unified Google Gemini Developer SDK.
- **`dotenv`:** Load credential profiles.
- **`GEMINI_API_KEY`:** Configured inside `.env` or globally.
