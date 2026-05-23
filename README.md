# 🌌 SAGA: The Novel Engineering Studio 🌌

SAGA is a high-fidelity, model-agnostic command-line writing assistant and autonomous novel engineering factory. Designed to run directly inside your favorite IDE, SAGA pair-programs with you—integrating creative narrative departmental agents (the Architect, Scribe, and Evaluator) with robust terminal status dashboards and multi-voice audiobook synthesis.

---

## 🌟 Key Features

*   **Premium TUI Split-View status Card:** Real-time tracking of active novel drafting progress, chapters, and word counts, alongside color-coded adversarial score gates and suggested next actions.
*   **Adversarial Score Gates:** Programmatic self-correction retry loops that automatically audit drafted chapters for POV filter words, slop clichés, and dialogue subtext using Gemini Pro/Flash before saving files.
*   **Autonomous YOLO Mode:** Hands-free, end-to-end novel engineering. Sit back and watch SAGA orchestrate outlines, seed beatsheets, draft chapters, update character lore profiles, and generate illustrations.
*   **Complete Publishing Pipeline:** Compile eBook containers (.ePUB), print typeset HTML pages, parse dialogue maps, and synthesize high-quality, multi-voice WAV audiobooks with Gemini native TTS prebuilt voices.
*   **Multi-Project State Isolation:** Absolute workspace isolation protecting your projects' story bibles and setting parameters, linked together by a centralized user-profile dashboard.

---

## 📂 Workspace Directory Structure

Every SAGA workspace is structured as a clean, standardized story vault:

```text
├── 00_Story_Bible/          # Source of truth for your story world
│   ├── characters/          # Markdown files outlining character profiles & voices
│   ├── settings/            # Location descriptions and environments
│   ├── market_analysis.md   # Cynical market strategy, red/blue ocean gaps
│   └── style_guide.md       # Voice profiles, pacing directives, and anti-slop rules
├── 01_Planning/             # Narrative architecture files
│   ├── premise.md           # Loglines, core themes, and value shifts
│   ├── outline.md           # High-level chapter structural outline
│   └── beats/               # Scene-by-scene beat sheets (e.g. chapter_01_beats.md)
├── 02_Drafting/             # Clean markdown chapter drafts (e.g. chapter_01.md)
├── 03_Review/               # Adversarial critique scorecard logs and edits
├── 04_Publishing/           # Generated ePUBs, print typeset books, and WAV audiobooks
└── .agent/                  # Specialized agent system instructions
```

---

## 🚀 Getting Started & Installation

### 1. Prerequisites
SAGA requires **Python 3.10 or higher** and a **Gemini Developer API Key**. 
Generate your API key for free on [Google AI Studio](https://aistudio.google.com/).

### 2. Quick Onboarding
1. Clone this repository to your desktop or workspace directory.
2. Duplicate `.env.example` and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and configure your API key:
   ```env
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY
   ```
4. Register SAGA globally into your terminal PATH:
   ```bash
   pip install --editable .
   ```

You can now summon SAGA anywhere in your terminal simply by running `saga`!

---

## 💻 CLI Commands Quick Reference

| Goal | Command | Description |
| :--- | :--- | :--- |
| **Summon SAGA / status** | `saga` or `saga --status` | Launches the interactive starting wizard or split-view status card. |
| **List All Books** | `saga --dashboard` | Renders a gold-accented double-bordered registry directory table. |
| **New Book setup** | `saga --init <folder>` | Seeds a fresh isolated novel directory with clean templates. |
| **Story Outline** | `saga --outline` | Initiates cynical market analysis and 6-beat chapter outlining. |
| **Chapter Draft** | `saga --draft <num>` | Pairs Scribe and Evaluator in self-correction retry loops. |
| **Compile & Publish** | `saga --publish` | Packs print typesets, ePUBs, speaker CSVs, and WAV audiobooks. |
| **Autonomous YOLO** | `saga --yolo` | Spins up the autonomous end-to-end novel factory. |
| **Configuration** | `saga --config` | Launches the interactive model and credentials editor. |

---

## 💖 Acknowledgments & Inspirations

SAGA is built on the shoulders of giants in the creative writing and developer tooling communities. We want to give special thanks to our core inspirations:

*   **The Nerdy Novelist:** For pioneering the structural planning, story-grid beatsheets, and developmental pair-drafting methodologies that serve as the foundation for the Scribe and Architect agents.
*   **Nous Research (`AutoNovel`):** For benchmarking creative multi-agent autonomous creative pipelines, demonstrating the power of adversarial AI storytelling loops.
*   **Claude Code (Anthropic):** For inspiring SAGA's premium terminal TUI split-column border layout designs and mathematical padding formats.
*   **Hermes-Agent:** For shaping the sleek, gold-accented double-bordered registry grid console displays.

---

## 📄 License

This repository is open-sourced under the permissive **[MIT License](LICENSE)**. Feel free to clone, edit, extend, and share SAGA with your beta testers!
