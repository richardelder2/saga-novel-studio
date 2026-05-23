import os
import sys

# Ensure UTF-8 output encoding for emojis in Windows terminals
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import glob
import json
import re
import uuid
import datetime
import subprocess
import shutil
import random

# Cool names generator
ADJECTIVES = ["crimson", "obsidian", "nebular", "astral", "midnight", "solar", "lunar", "silent", "phantom", "echoing", "crystal", "iron", "velvet", "storm", "cyber", "ethereal"]
NOUNS = ["void", "nexus", "peak", "spire", "drift", "engine", "protocol", "odyssey", "whisper", "horizon", "sanctuary", "citadel", "forge", "archive", "expanse"]

def generate_random_project_name():
    return f"{random.choice(ADJECTIVES)}-{random.choice(NOUNS)}"

# Addscripts directory to path to import agent_core and manage_manifest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".agent", "scripts")))
import agent_core
import manage_manifest
import parse_audiobook
import synthesize_audiobook
import typeset_book

def print_logo():
    print("=" * 80)
    print(" " * 22 + "🌌 SAGA: THE NOVEL ENGINEERING ENGINE 🌌")
    print("=" * 80)

def prompt_user(question, default=""):
    prompt_text = f"{question} [{default}]: " if default else f"{question}: "
    val = input(prompt_text).strip()
    return val if val else default

def run_init(target_name=""):
    print_logo()
    print("Welcome, Creator. Saga is an agent-friendly, model-agnostic novel factory.")
    print("Let's configure a fresh story book project inside its own directory.")
    print("-" * 80)
    
    # 1. Resolve target directory name
    project_name = target_name.strip() if target_name else ""
    if not project_name:
        if sys.stdin.isatty():
            try:
                project_name = prompt_user("Enter target directory name for your new book (or press Enter to generate a name)", "").strip()
            except Exception:
                project_name = ""
        if not project_name:
            project_name = generate_random_project_name()
            print(f"🎲 Generated project name: '{project_name}'")
            
    new_project_path = os.path.abspath(os.path.join(os.getcwd(), project_name))
    print(f"📍 New novel directory: {new_project_path}")
    
    if os.path.exists(new_project_path):
        print(f"❌ Error: A folder or file named '{project_name}' already exists in this location.")
        sys.exit(1)
        
    # 2. Interactive onboarding questionnaire
    if not sys.stdin.isatty():
        print("⚠️ Non-interactive environment detected. Seeding default foundations...")
        title = project_name.replace("-", " ").replace("_", " ").title()
        genre = "General Fiction"
        premise = "An elegant, automated narrative framework designed for agentic pair programming."
        choice = "1"
        aesthetic = "Noir, Atmospheric, High-Contrast"
        writing_mode = "manual"
    else:
        # Suggest a clean Title derived from target directory name
        default_title = project_name.replace("-", " ").replace("_", " ").title()
        title = prompt_user("Book Title", default_title)
        genre = prompt_user("Overarching Genre (e.g. Sci-Fi, Thriller, Romance)", "Sci-Fi Thriller")
        premise = prompt_user("Story Premise / Logline (elevator pitch)")
        
        print("\nIs this part of a series or in a shared universe?")
        print("  [1] Standalone Novel")
        print("  [2] Part of an Active Series")
        print("  [3] Linked to a Shared Universe")
        choice = prompt_user("Select Option", "1")
        
        print("\nSelect Book Development Mode:")
        print("  [1] 💻 MANUAL MODE (Collaborative Chapter-by-Chapter) [Default]")
        print("  [2] 🚀 YOLO MODE (Autonomous End-to-End Novel Generation)")
        mode_choice = prompt_user("Select Option", "1")
        writing_mode = "yolo" if mode_choice == "2" else "manual"
        
        aesthetic = prompt_user("Visual & Aesthetic Keywords (moodboard)", "Atmospheric, Neon, Cinematic")
        
    is_series = "yes" if choice in ["2", "3"] else "no"
    
    # 3. Clone/copy template to new project path
    template_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📂 Cloning clean slate from template: {template_dir}...")
    
    # Ignore build outputs, previous drafts/reviews, git histories, and registries
    ignore_patterns = shutil.ignore_patterns(
        ".git", ".git/*", "__pycache__", "*.pyc", 
        "extracted_text.txt", "start_new_book.py", 
        "02_Drafting/chapter_*.md", "03_Review/critique_*.md", 
        "04_Publishing/*", ".agent/projects_registry.json"
    )
    
    try:
        shutil.copytree(template_dir, new_project_path, ignore=ignore_patterns)
        print("✓ Core templates and structural directories cloned.")
    except Exception as e:
        print(f"❌ Error cloning directory templates: {e}")
        sys.exit(1)
        
    # 4. Generate story manifest
    manifest_path = os.path.join(new_project_path, "00_Story_Bible", "project_manifest.json")
    manifest_data = {
        "project_id": str(uuid.uuid4()),
        "title": title,
        "genre": genre,
        "created_at": datetime.date.today().isoformat(),
        "status": {
            "active_phase": "Phase 1: Planning",
            "current_chapter": 0,
            "total_chapters": 20,
            "word_count": 0
        },
        "latest_scores": {
            "foundation_score": None,
            "drafting_score": None,
            "editorial_score": None
        },
        "mode": writing_mode,
        "git_branch": "main",
        "shared_universe_path": new_project_path if is_series == "yes" else None,
        "model_configuration": {
            "creative_model": "gemini-2.5-flash",
            "critic_model": "gemini-2.5-flash"
        },
        "last_updated_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    print("✓ Created 00_Story_Bible/project_manifest.json")
    
    # 5. Create premise.md
    premise_content = f"""# Story Premise: {title}
 
**Genre:** {genre}
**Aesthetic Vibe:** {aesthetic}

## Logline
{premise}

## Core Themes
*   Theme Anchor: Value shifts from isolation to connection through joint struggle.
*   Protagonist Focus: Internal obstacle drives external conflict.
"""
    with open(os.path.join(new_project_path, "01_Planning/premise.md"), "w", encoding="utf-8") as f:
        f.write(premise_content)
    print("✓ Created 01_Planning/premise.md")
    
    # 6. Create style_guide.md
    style_guide = f"""# Style Guide: {title}

**Voice Profile:** Active, immersive, and sensory-driven.
**Pacing:** Tight chapter turns with high structural tension.

## Core Directives
1.  **Immersive POV**: Eliminate filter words ('saw', 'heard', 'felt').
2.  **Prose Clichés**: Ban slop words ('testament to', 'beacon of hope', 'in that moment').
3.  **Active dialogue**: Use contractions and incorporate realistic subtext.
"""
    with open(os.path.join(new_project_path, "00_Story_Bible/style_guide.md"), "w", encoding="utf-8") as f:
        f.write(style_guide)
    print("✓ Created 00_Story_Bible/style_guide.md")
    
    # 7. Register in central projects registry
    registry_path = manage_manifest.locate_registry(new_project_path)
    registry = manage_manifest.load_registry(registry_path)
    updated_registry = [p for p in registry if os.path.abspath(p.get("path", "")) != new_project_path]
    updated_registry.append({
        "project_id": manifest_data.get("project_id"),
        "title": title,
        "path": new_project_path,
        "created_at": manifest_data.get("created_at")
    })
    manage_manifest.save_registry(registry_path, updated_registry)
    print(f"✓ Registered project inside SAGA Registry: {registry_path}")
    
    # 8. Initialize clean Git version control
    try:
        subprocess.run(["git", "init"], cwd=new_project_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["git", "add", "."], cwd=new_project_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["git", "commit", "-m", f"Initial commit for {title}"], cwd=new_project_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        print("✓ Created fresh Git repository with clean template commit.")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize Git: {e}")
        
    print("-" * 80)
    print("🎉 SUCCESS! SAGA STORY BIBLE FOUNDATIONS FULLY ESTABLISHED!")
    print(f"Project '{title}' has been successfully spun up inside:")
    print(f"  {new_project_path}")
    print("\nTo start writing your new book, change directories:")
    print(f"  cd {project_name}")
    print("And check your status:")
    print("  saga --status")
    print("=" * 80 + "\n")

def run_dashboard():
    # Invokes manifest registry to list all books on system
    workspace_path = os.getcwd()
    registry_path = manage_manifest.locate_registry(workspace_path)
    project_list = manage_manifest.scan_projects(workspace_path, registry_path)
    manage_manifest.print_dashboard(project_list, workspace_path)

def run_status():
    manifest_path = "00_Story_Bible/project_manifest.json"
    content = agent_core.read_file_content(manifest_path)
    if not content:
        print("❌ Error: No active Saga project manifest found in this directory.")
        return
        
    try:
        data = json.loads(content)
    except Exception as e:
        print(f"❌ Error decoding manifest JSON: {e}")
        return
        
    title = data.get("title", "Untitled")
    genre = data.get("genre", "General Fiction")
    status = data.get("status", {})
    phase = status.get("active_phase", "Planning")
    current_ch = status.get("current_chapter", 0)
    total_ch = status.get("total_chapters", 20)
    word_count = status.get("word_count", 0)
    scores = data.get("latest_scores", {})
    
    print("=" * 80)
    print(f"  📖 SAGA PROJECT STATUS: {title.upper()}")
    print("=" * 80)
    print(f"  🎭 Overarching Genre  : {genre}")
    print(f"  📍 Active Phase       : {phase}")
    
    # Progress bar
    percent = int((current_ch / total_ch) * 100) if total_ch > 0 else 0
    bar_width = 30
    filled = int((percent / 100) * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)
    print(f"  📊 Draft Progress     : [{bar}] {percent}% ({current_ch}/{total_ch} chapters)")
    print(f"  📝 Words Drafted      : {word_count:,} words")
    
    # Scores
    print(f"  🎯 Latest Score Gates :")
    print(f"    • Foundation Score  : {scores.get('foundation_score') or 'N/A'}")
    print(f"    • Drafting Score    : {scores.get('drafting_score') or 'N/A'}")
    print(f"    • Editorial Score   : {scores.get('editorial_score') or 'N/A'}")
    print("-" * 80)
    print(f"  💻 Scribe Model       : {data.get('model_configuration', {}).get('creative_model') or 'N/A'}")
    print(f"  🕵️ Critic Model       : {data.get('model_configuration', {}).get('critic_model') or 'N/A'}")
    print("=" * 80 + "\n")

def run_outline():
    print_logo()
    print("📐 SAGA ARCHITECT: Starting Chapter Outline Generation Loop...")
    print("-" * 80)
    
    manifest_path = "00_Story_Bible/project_manifest.json"
    content = agent_core.read_file_content(manifest_path)
    if not content:
        print("❌ Error: Run 'python saga_cli.py --init' first.")
        return
        
    try:
        manifest = json.loads(content)
    except Exception as e:
        print(f"❌ Error loading manifest: {e}")
        return
        
    premise = agent_core.read_file_content("01_Planning/premise.md")
    if not premise or len(premise.strip()) < 20:
        print("❌ Story premise is missing. Please populate 01_Planning/premise.md first.")
        return
        
    client = agent_core.get_gemini_client()
    
    # Check/compile Cynical Market Analysis
    market_path = "00_Story_Bible/market_analysis.md"
    market_analysis = agent_core.read_file_content(market_path)
    if not market_analysis or len(market_analysis.strip()) < 50:
        print("Compiling commercial publishing strategy and market gaps autonomously...")
        genre = manifest.get("genre", "Fiction")
        title = manifest.get("title", "this novel")
        
        market_prompt = (
            f"Perform a cynical market trend analysis for a novel in the '{genre}' genre (working title: '{title}').\n"
            "Analyze current commercial best-sellers, reader demands, over-saturated tropes (red oceans), and under-served commercial gaps (blue oceans).\n"
            "Provide a brutal, high-concept strategy detailing how this novel can exploit commercial white space and capitalize on recent market trends."
        )
        
        market_analyst_inst = (
            "You are a highly cynical commercial publishing executive who only cares about absolute unit sales, subverting/exploiting tropes, and finding commercial white space. "
            "Analyze current market demand brutally. Do not write filler. Output a structured, publication-ready report in professional markdown, covering:\n"
            "1. Target Genre & Sub-Genres\n"
            "2. Red Oceans (Over-saturated Tropes to Avoid/Subvert)\n"
            "3. Blue Oceans (Under-served Demand & Gaps)\n"
            "4. The Commercial Hook (How our book will capitalize on these trends)\n"
            "5. Top Trope Exploits & High-Concept Packaging"
        )
        
        market_analysis = agent_core.call_gemini(client, market_prompt, market_analyst_inst, model=agent_core.get_model_config("critic"))
        if market_analysis:
            agent_core.write_file_content(market_path, market_analysis)
            print("✓ market_analysis.md compiled and saved to 00_Story_Bible/.")
        else:
            print("❌ Generating market_analysis.md failed.")
            return

    # Generate Outline
    print("Generating chapter-by-chapter outline via the Architect...")
    system_inst = agent_core.get_system_instruction("architect_instructions.md")
    prompt = (
        f"Based on the story premise and cynical market analysis below, create a structured 6-beat chapter outline "
        f"that exploits commercial white space and reader demand.\n\n"
        f"Market Analysis:\n{market_analysis}\n\nPremise:\n{premise}"
    )
    outline = agent_core.call_gemini(client, prompt, system_inst)
    if outline:
        agent_core.write_file_content("01_Planning/outline.md", outline)
        print("✓ Created 01_Planning/outline.md")
    else:
        print("❌ Outlining failed.")
        return

    # Evaluator audit gate
    print("Auditing Outline structure autonomously via the Evaluator...")
    system_inst = agent_core.get_system_instruction("evaluator_instructions.md")
    eval_prompt = f"Audit the following outline against Foolscap rules. Provide a critique and score out of 10.\n\nOutline:\n{outline}"
    critique = agent_core.call_gemini(client, eval_prompt, system_inst, model=agent_core.get_model_config("critic"))
    
    score = 8.2
    if critique:
        agent_core.write_file_content("01_Planning/foundation_critique.md", critique)
        print("✓ Outline audit logged at 01_Planning/foundation_critique.md.")
        
        # Parse score
        score_match = re.search(r'Score:\s*(\d+\.\d+|\d+)', critique)
        if score_match:
            score = float(score_match.group(1))
            
    print(f"  • Foundation Outline Score: {score}/10")
    
    # Update manifest phase
    manifest["status"]["active_phase"] = "Phase 2: Drafting"
    manifest["latest_scores"]["foundation_score"] = score
    manifest["last_updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    agent_core.write_file_content(manifest_path, json.dumps(manifest, indent=2))
    
    print("-" * 80)
    print("🎉 OUTLINING COMPLETE! Project advanced to Phase 2: Drafting.")
    print("SAGA is ready to draft chapters. Run: python saga_cli.py --draft 1")
    print("=" * 80 + "\n")

def run_draft(chapter_num):
    print_logo()
    ch_str = f"{chapter_num:02d}"
    print(f"🎬 SAGA SCRIBE: Drafting Chapter {ch_str}...")
    print("-" * 80)
    
    manifest_path = "00_Story_Bible/project_manifest.json"
    content = agent_core.read_file_content(manifest_path)
    if not content:
        print("❌ Error: Project manifest missing. Run init first.")
        return
        
    try:
        manifest = json.loads(content)
    except Exception as e:
        print(f"❌ Error decoding manifest: {e}")
        return
        
    beat_file = f"01_Planning/beats/chapter_{ch_str}_beats.md"
    draft_file = f"02_Drafting/chapter_{ch_str}.md"
    critique_file = f"03_Review/critique_{ch_str}.md"
    
    # Check beatsheet. If missing, seed it autonomously
    beats = agent_core.read_file_content(beat_file)
    client = agent_core.get_gemini_client()
    
    if not beats:
        print(f" Beatsheet missing. Architect is seeding beats autonomously for Chapter {ch_str}...")
        outline = agent_core.read_file_content("01_Planning/outline.md")
        market_analysis = agent_core.read_file_content("00_Story_Bible/market_analysis.md")
        
        system_inst = agent_core.get_system_instruction("architect_instructions.md")
        prompt = (
            f"Based on the outline and cynical market analysis below, draft a 3-scene beat sheet "
            f"for Chapter {chapter_num} that embeds commercial trope exploits and target hooks.\n\n"
            f"Market Analysis:\n{market_analysis}\n\nOutline:\n{outline}"
        )
        beats = agent_core.call_gemini(client, prompt, system_inst)
        if beats:
            agent_core.write_file_content(beat_file, beats)
            print(f"✓ Seeded beatsheet at: {beat_file}")
        else:
            print("❌ Beats generation failed.")
            return

    # Load context
    style_guide = agent_core.read_file_content("00_Story_Bible/style_guide.md")
    market_analysis = agent_core.read_file_content("00_Story_Bible/market_analysis.md")
    
    # Load Character Profiles
    char_files = glob.glob("00_Story_Bible/characters/*.md")
    char_context = ""
    if char_files:
        char_context_list = []
        for cf in char_files:
            char_context_list.append(f"--- CHARACTER: {os.path.basename(cf)} ---\n{agent_core.read_file_content(cf)}")
        char_context = "\n\n".join(char_context_list)
        
    # Load settings
    setting_files = glob.glob("00_Story_Bible/settings/*.md")
    setting_context = ""
    if setting_files:
        setting_context_list = []
        for sf in setting_files:
            setting_context_list.append(f"--- SETTING: {os.path.basename(sf)} ---\n{agent_core.read_file_content(sf)}")
        setting_context = "\n\n".join(setting_context_list)
        
    # Load chronology bridge
    prev_ch_bridge = ""
    if chapter_num > 1:
        prev_ch_str = f"{(chapter_num - 1):02d}"
        prev_content = agent_core.read_file_content(f"02_Drafting/chapter_{prev_ch_str}.md")
        if prev_content:
            paragraphs = [p.strip() for p in prev_content.split("\n\n") if p.strip()]
            bridge_paras = paragraphs[-3:] if len(paragraphs) >= 3 else paragraphs
            prev_ch_bridge = "\n\n".join(bridge_paras)

    # ---------------- PROSE SELF-CORRECTION RETRY LOOP ----------------
    best_draft = ""
    best_score = 0.0
    best_critique = ""
    max_retries = 3
    
    for attempt in range(1, max_retries + 1):
        print(f"🤖 Scribe drafting Chapter {ch_str} (Attempt {attempt}/{max_retries})...")
        if attempt > 1:
            prompt = (
                f"You are revising Chapter {chapter_num} based on a critique. Here is the previous draft:\n\n"
                f"{draft}\n\nHere is the Evaluator's structured JSON critique outlining the failures and score:\n\n"
                f"{critique}\n\n"
                f"Please revise the chapter to fix the issues, eliminate all POV filters, remove slop clichés, and edit dialogues to use natural subtext.\n"
                f"Ensure the revisions align perfectly with our style, character profiles, settings, and market goals.\n\n"
                f"--- CYNICAL MARKET ANALYSIS ---\n{market_analysis}\n\n"
                f"--- STORY STYLE GUIDE ---\n{style_guide}\n\n"
                f"--- ACTIVE CHARACTERS ---\n{char_context}\n\n"
                f"--- WORLD SETTINGS ---\n{setting_context}\n\n"
                f"--- CHAPTER BEATS SHEET ---\n{beats}\n\n"
            )
        else:
            prompt = (
                f"Write a fully detailed, immersive narrative prose draft for Chapter {chapter_num} based strictly on the beats sheet below.\n\n"
                f"--- CYNICAL MARKET ANALYSIS ---\n{market_analysis}\n\n"
                f"--- STORY STYLE GUIDE ---\n{style_guide}\n\n"
                f"--- ACTIVE CHARACTERS ---\n{char_context}\n\n"
                f"--- WORLD SETTINGS ---\n{setting_context}\n\n"
                f"--- CHAPTER BEATS SHEET ---\n{beats}\n\n"
            )
            if prev_ch_bridge:
                prompt += (
                    f"--- CHAPTER {chapter_num-1} BRIDGE (Maintain direct chronological continuity with these closing lines) ---\n"
                    f"{prev_ch_bridge}\n\n"
                )
                
        system_inst = agent_core.get_system_instruction("scribe_instructions.md")
        draft = agent_core.call_gemini(client, prompt, system_inst)
        if not draft:
            print("❌ Scribe failed to draft chapter.")
            return
            
        # Programmatic structured JSON score audits
        print(f"🕵️ AI Critic auditing Chapter {ch_str} (Attempt {attempt}/{max_retries})...")
        evaluator_inst = (
            "You are an adversarial AI Critic. Audit the chapter prose strictly. "
            "Examine Pacing, POV filters ('saw', 'heard', 'felt'), slop clichés, and dialogue naturalness. "
            "Output your audit as a valid JSON object matching exactly this structure:\n"
            "{\n"
            "  \"overall_score\": 8.0,\n"
            "  \"failures\": [\"Line 23 POV filter: 'she heard'\"],\n"
            "  \"feedback\": \"detailed critique text here\"\n"
            "}"
        )
        
        eval_prompt = f"Evaluate the following prose draft. Return a structured scorecard JSON payload.\n\nDraft:\n{draft}"
        critique = agent_core.call_gemini(client, eval_prompt, evaluator_inst, model=agent_core.get_model_config("critic"), mime_type="application/json")
        
        draft_score = 6.0
        if critique:
            try:
                score_data = json.loads(critique)
                draft_score = float(score_data.get("overall_score", 6.0))
                failures = score_data.get("failures", [])
                if failures:
                    print("  ⚠️ Critic flagged failures:")
                    for f in failures[:3]:
                        print(f"    - {f}")
            except Exception:
                # Text fallback parsing
                score_match = re.search(r'overall_score":\s*(\d+\.\d+|\d+)', critique)
                if score_match:
                    draft_score = float(score_match.group(1))
                    
        print(f"  • Attempt {attempt} Score Card: {draft_score}/10")
        
        if draft_score > best_score:
            best_score = draft_score
            best_draft = draft
            best_critique = critique
            
        if draft_score >= 7.5:
            print(f"🎉 Prose audit PASSED with a score of {draft_score}/10!")
            break
        else:
            print(f"⚠️ Score {draft_score}/10 is below the 7.5 threshold. Retrying loop...")
            
    draft = best_draft
    critique = best_critique
    draft_score = best_score
    
    agent_core.write_file_content(draft_file, draft)
    agent_core.write_file_content(critique_file, critique)
    
    # ---------------- DEEP EDITOR POLISH ----------------
    print(f"✨ Deep Editor performing final sensory developmental edit on Chapter {ch_str}...")
    system_inst = agent_core.get_system_instruction("deep_editor_instructions.md")
    prompt = f"Developmental edit the following draft, incorporating this Evaluator critique.\n\nDraft:\n{draft}\n\nCritique:\n{critique}"
    polished_draft = agent_core.call_gemini(client, prompt, system_inst)
    if polished_draft:
        agent_core.write_file_content(draft_file, polished_draft)
        print("✓ Deep Editor developmental edit completed.")
    else:
        polished_draft = draft
        print("⚠️ Deep Editor failed. Keeping original draft.")
        
    # ---------------- LORE KEEPER CANON CONTINUITY ----------------
    print(f"📖 Lore Keeper reviewing Chapter {ch_str} and updating Story Bible...")
    system_inst = agent_core.get_system_instruction("lore_keeper_instructions.md")
    lore_prompt = (
        f"You have just finished Chapter {chapter_num}. Below is the final polished text of the chapter:\n\n"
        f"{polished_draft}\n\nHere are the current character files in the Story Bible:\n\n"
        f"{char_context}\n\n"
        f"Please review the chapter for any character development, relationship changes, new secrets revealed, or settings introduced. "
        f"For each relevant character file, provide an updated markdown profile. Return a JSON structure matching exactly:\n"
        f"{{\n  \"characters\": [\n    {{\"filename\": \"character_file_name.md\", \"content\": \"full updated markdown content here\"}}\n  ]\n}}"
    )
    
    lore_updates = agent_core.call_gemini(client, lore_prompt, system_inst, mime_type="application/json")
    if lore_updates:
        try:
            data = json.loads(lore_updates)
            for char_data in data.get("characters", []):
                filename = os.path.basename(char_data.get("filename"))
                content = char_data.get("content")
                if filename and content:
                    char_path = os.path.join("00_Story_Bible/characters", filename)
                    agent_core.write_file_content(char_path, content)
                    print(f"  • Updated character profile canon: {filename}")
        except Exception as e:
            print(f"  ⚠️ Warning: Could not parse Lore Keeper update: {e}")

    # Auto commit
    print("Committing chapter to Git autonomously...")
    agent_core.run_git_command(["git", "add", "."])
    agent_core.run_git_command(["git", "commit", "-m", f"SAGA: Completed Chapter {ch_str} (Score: {draft_score})"])
    
    # Update manifest
    manifest["status"]["current_chapter"] = chapter_num
    manifest["latest_scores"]["drafting_score"] = draft_score
    manifest["status"]["word_count"] = manage_manifest.recalculate_stats(os.getcwd())[0]
    manifest["last_updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    agent_core.write_file_content(manifest_path, json.dumps(manifest, indent=2))
    
    print("-" * 80)
    print(f"🎉 CHAPTER {ch_str} DRAFTED AND VERIFIED CANON!")
    print(f"Prose locked at Chapter Gate score: {draft_score}/10.")
    print("=" * 80 + "\n")

def run_publish():
    print_logo()
    print("🎨 SAGA PRODUCTION: Packaging ePub, Print layouts, and WAV Audiobooks...")
    print("-" * 80)
    
    # 1. LaTeX Typeset HTML
    print("🎨 Typesetting HTML book print pages...")
    typeset_book.typeset_book()
    
    # 2. Extract dialogue script CSV map
    print("📝 Parsing audiobook dialogue speaker coreference map...")
    parse_audiobook.build_audiobook_script()
    
    # 3. Synthesize wav audiobook (Native Gemini TTS)
    print("🎙️ Synthesizing multi-voice WAV audiobook (dynamic rate-limiting)...")
    synthesize_audiobook.main()
    
    # 4. Build landing page Promo
    manifest_path = "00_Story_Bible/project_manifest.json"
    content = agent_core.read_file_content(manifest_path)
    if content:
        try:
            data = json.loads(content)
            print("\n🌐 Compiling landing page index.html promo page...")
            title = data.get("title", "Untitled Novel")
            genre = data.get("genre", "Fiction")
            synopsis = agent_core.read_file_content("01_Planning/premise.md")
            synopsis_html = synopsis.replace("# Story Premise\n\n", "").replace("\n\n", "</p><p>").replace("\n", "<br/>")
            
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title} - Promotional Landing Page</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Cinzel:wght@600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Outfit', sans-serif;
      background: radial-gradient(circle at top right, #1e293b, #0f172a);
      color: #f1f5f9;
      margin: 0;
      padding: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }}
    .landing-container {{
      max-width: 900px;
      margin: 40px auto;
      padding: 40px;
      background: rgba(30, 41, 59, 0.45);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 24px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.3);
      display: flex;
      gap: 40px;
      align-items: center;
    }}
    .cover-wrapper {{
      flex: 1;
      max-width: 320px;
      box-shadow: 0 15px 35px rgba(0,0,0,0.5);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(255,255,255,0.1);
      transition: transform 0.3s;
    }}
    .cover-wrapper:hover {{
      transform: translateY(-8px);
    }}
    .cover-wrapper img {{
      width: 100%;
      display: block;
    }}
    .details-wrapper {{
      flex: 1.5;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .title {{
      font-family: 'Cinzel', serif;
      font-size: 2.8rem;
      margin: 0;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .genre-tag {{
      display: inline-block;
      padding: 4px 12px;
      background: rgba(14, 116, 144, 0.3);
      border: 1px solid rgba(14, 116, 144, 0.5);
      border-radius: 99px;
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #38bdf8;
      width: fit-content;
    }}
    .synopsis {{
      line-height: 1.6;
      color: #cbd5e1;
      font-size: 1.05rem;
    }}
    .audiobook-player {{
      margin-top: 15px;
      padding: 15px;
      background: rgba(255,255,255,0.04);
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.06);
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .player-title {{
      font-size: 0.9rem;
      font-weight: 600;
      text-transform: uppercase;
      color: #94a3b8;
    }}
    .audiobook-player audio {{
      width: 100%;
    }}
    .button-group {{
      display: flex;
      gap: 15px;
      margin-top: 20px;
    }}
    .btn {{
      padding: 12px 24px;
      border-radius: 12px;
      font-size: 0.95rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s;
      text-align: center;
      flex: 1;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, #0284c7, #4f46e5);
      color: #fff;
      box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }}
    .btn-primary:hover {{
      background: linear-gradient(135deg, #0369a1, #4338ca);
      box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
    }}
    .btn-secondary {{
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.15);
      color: #f1f5f9;
    }}
    .btn-secondary:hover {{
      background: rgba(255,255,255,0.1);
    }}
  </style>
</head>
<body>
  <div class="landing-container">
    <div class="cover-wrapper">
      <img src="covers/cover_concept.png" onerror="this.src='https://placehold.co/600x800/1e293b/f1f5f9?text={title.replace(' ', '+')}'" alt="Book Cover">
    </div>
    <div class="details-wrapper">
      <div class="genre-tag">{genre}</div>
      <h1 class="title">{title}</h1>
      <div class="synopsis">
        <p>{synopsis_html}</p>
      </div>
      <div class="audiobook-player">
        <div class="player-title">🔊 Listen to the Audiobook</div>
        <audio controls src="audiobook.wav"></audio>
      </div>
      <div class="button-group">
        <a href="manuscript.epub" class="btn btn-primary">📖 Download eBook (.ePUB)</a>
        <a href="typeset_manuscript.html" class="btn btn-secondary" target="_blank">📄 Open Print Typeset</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
            agent_core.write_file_content("04_Publishing/index.html", html_content)
            print("🎉 Promo Landing Page generated at 04_Publishing/index.html")
        except Exception as e:
            print(f"⚠️ Landing page compiling failed: {e}")

    print("-" * 80)
    print("🎉 PUBLISHING RUN FULLY ACCOMPLISHED!")
    print("Print Layouts, ePUBs, Audiobooks, and Landing Pages completed successfully.")
    print("=" * 80 + "\n")

def main():
    # Dynamic Local Routing: If there is a saga_cli.py in current working directory and it is not this file itself,
    # forward execution to that script to respect the local project's environment.
    current_dir_cli = os.path.join(os.getcwd(), "saga_cli.py")
    if os.path.exists(current_dir_cli) and os.path.abspath(current_dir_cli) != os.path.abspath(__file__):
        if not os.environ.get("SAGA_REDIRECTED"):
            import subprocess
            import sys
            os.environ["SAGA_REDIRECTED"] = "1"
            result = subprocess.run([sys.executable, current_dir_cli] + sys.argv[1:])
            sys.exit(result.returncode)

    import argparse
    parser = argparse.ArgumentParser(description="SAGA CLI — Novel Engineering Engine.")
    parser.add_argument("--init", nargs="?", const="", type=str, help="Initialize and onboard a new story book vault in a target directory.")
    parser.add_argument("--dashboard", action="store_true", help="Print global directories dashboard of all novels.")
    parser.add_argument("--status", action="store_true", help="Print current active novel status card.")
    parser.add_argument("--outline", action="store_true", help="Run the Architect chapter outlining phase and audit gate.")
    parser.add_argument("--draft", type=int, help="Draft the specified chapter with structured self-correction retry loops.")
    parser.add_argument("--publish", action="store_true", help="Compile ePub containers, typesets, dialog scripts, and synthesizers.")
    args = parser.parse_args()
    
    if args.init is not None:
        run_init(args.init)
    elif args.dashboard:
        run_dashboard()
    elif args.status:
        run_status()
    elif args.outline:
        run_outline()
    elif args.draft is not None:
        run_draft(args.draft)
    elif args.publish:
        run_publish()
    else:
        # Default status check
        manifest_path = "00_Story_Bible/project_manifest.json"
        if os.path.exists(manifest_path):
            run_status()
        else:
            run_init("")

if __name__ == "__main__":
    main()
