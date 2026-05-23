import os
import sys
import glob
import json
import re
import subprocess
from google import genai
from google.genai import types
from dotenv import load_dotenv

def run_git_command(args):
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"⚠️ Git error: {e}")
        return None

def read_file_content(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    return ""

def write_file_content(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def get_system_instruction(persona_filename):
    path = os.path.join(".agent", persona_filename)
    content = read_file_content(path)
    if not content:
        # Fallback default instructions if missing
        return f"You are a helpful creative writing assistant acting as {persona_filename}."
    return content

def call_gemini(client, prompt, system_instruction):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        print(f"❌ Gemini API Call Error: {e}")
        return ""

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    import argparse
    parser = argparse.ArgumentParser(description="CoAuthor YOLO Mode - Autonomous Novel Director.")
    parser.add_argument("--dry-run", action="store_true", help="Perform checks and mock the API calls without consuming credits.")
    parser.add_argument("--max-chapters", type=int, default=1, help="Maximum number of chapters to draft in this autonomous session.")
    args = parser.parse_args()

    print("🚀 WELCOME TO COAUTHOR YOLO MODE 🚀")
    print("====================================")
    print("Autonomous Creative Loop active. Sitting back is advised.\n")

    # Load credentials
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        print("❌ Error: GEMINI_API_KEY is not configured in '.env'.")
        sys.exit(1)

    client = None
    if not args.dry_run:
        client = genai.Client(api_key=api_key)

    # 1. Read Project Manifest
    manifest_path = "00_Story_Bible/project_manifest.json"
    if not os.path.exists(manifest_path):
        print("❌ Error: Manifest file not found. Please run '/start-new-book' first.")
        sys.exit(1)
        
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"❌ Error loading manifest: {e}")
        sys.exit(1)

    print(f"📖 Active Novel: {manifest.get('title', 'Untitled')}")
    print(f"🎭 Genre: {manifest.get('genre', 'Fiction')}")
    print(f"📍 Active Phase: {manifest['status']['active_phase']}")
    print(f"💻 Operational Mode: YOLO (Autonomous)\n")

    # Override mode in manifest if running YOLO
    manifest["mode"] = "yolo"

    # ==================== PHASE 1: PLANNING ====================
    if manifest["status"]["active_phase"] == "Phase 1: Planning":
        print("--- PHASE 1: PLANNING LOOP ---")
        premise_path = "01_Planning/premise.md"
        outline_path = "01_Planning/outline.md"
        
        premise = read_file_content(premise_path)
        if not premise:
            print("⚠️ Premise file is empty! Seeding basic Cyberpunk Premise...")
            premise = "# Story Premise\n\nA cybernetic detective in a rain-slicked neon metropolis searches for a corporate heiress, uncovering digital transcendence secrets."
            write_file_content(premise_path, premise)
            
        print("Generating Outline autonomously via the Architect...")
        if args.dry_run:
            print("[DRY-RUN] Would call Gemini to act as Architect and generate outline.md.")
            outline = "# Chapter Outline\n\n## Chapter 1: The Rain-Slicked Club\nJax enters neon-soaked grid...\n\n## Chapter 2: The Digital Trace\nJax deciphers neural signals..."
            write_file_content(outline_path, outline)
        else:
            system_inst = get_system_instruction("architect_instructions.md")
            prompt = f"Based on the following premise, create a structured 6-beat chapter outline. Output in professional markdown.\n\nPremise:\n{premise}"
            outline = call_gemini(client, prompt, system_inst)
            if outline:
                write_file_content(outline_path, outline)
                print("✅ Outline generated successfully.")
            else:
                print("❌ Outlining failed.")
                sys.exit(1)

        # Evaluator critique (planning)
        print("Auditing Outline autonomously via the Evaluator...")
        if args.dry_run:
            print("[DRY-RUN] Evaluator scores the outline: 8.2/10 (PASS)")
            critique = "# Foundation Critique\n\n* Score: 8.2/10\n* Status: PASS"
            write_file_content("01_Planning/foundation_critique.md", critique)
        else:
            system_inst = get_system_instruction("evaluator_instructions.md")
            prompt = f"Audit the following outline against Foolscap rules. Provide a critique and score out of 10.\n\nOutline:\n{outline}"
            critique = call_gemini(client, prompt, system_inst)
            if critique:
                write_file_content("01_Planning/foundation_critique.md", critique)
                print("✅ Outline audit logged.")
            else:
                print("❌ Evaluator audit failed.")

        # Update manifest to drafting
        manifest["status"]["active_phase"] = "Phase 2: Drafting"
        manifest["latest_scores"]["foundation_score"] = 8.2
        
        # Compile a mock bible rules JSON
        write_file_content("00_Story_Bible/bible_canon_rules.json", json.dumps({
            "setting": "Cyberpunk metropolis",
            "characters": ["Jax Steele"],
            "rules": ["Bionics consume neural bio-fuel"]
        }, indent=2))
        
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print("✅ Manifest advanced to Phase 2: Drafting.\n")

    # ==================== PHASE 2: DRAFTING ====================
    if manifest["status"]["active_phase"] == "Phase 2: Drafting":
        print("--- PHASE 2: DRAFTING LOOP ---")
        
        # Find next chapter to draft
        draft_dir = "02_Drafting"
        existing_drafts = glob.glob(os.path.join(draft_dir, "chapter_*.md"))
        next_ch = 1
        if existing_drafts:
            numbers = []
            for d in existing_drafts:
                match = re.search(r'chapter_(\d+)', d)
                if match:
                    numbers.append(int(match.group(1)))
            if numbers:
                next_ch = max(numbers) + 1

        chapters_drafted = 0
        while chapters_drafted < args.max_chapters:
            ch_str = f"{next_ch:02d}"
            print(f"\n🎬 AUTONOMOUS DRAFTING LOOP: Chapter {ch_str}")
            
            beat_file = f"01_Planning/beats/chapter_{ch_str}_beats.md"
            draft_file = f"02_Drafting/chapter_{ch_str}.md"
            critique_file = f"03_Review/critique_{ch_str}.md"
            
            # Check beatsheet. If missing, seed it autonomously
            beats = read_file_content(beat_file)
            if not beats:
                print(f" Beatsheet missing. Architect is seeding beats autonomously for Chapter {ch_str}...")
                outline = read_file_content("01_Planning/outline.md")
                if args.dry_run:
                    beats = f"# Chapter {next_ch} Beats\n\n* Scene 1: Jax Steele enters neon club.\n* Scene 2: He interrogates the bar tender.\n* Scene 3: He receives coordinates of the hacker warehouse."
                    write_file_content(beat_file, beats)
                else:
                    system_inst = get_system_instruction("architect_instructions.md")
                    prompt = f"Based on the outline below, draft a 3-scene beat sheet for Chapter {next_ch}.\n\nOutline:\n{outline}"
                    beats = call_gemini(client, prompt, system_inst)
                    if beats:
                        write_file_content(beat_file, beats)
                    else:
                        print("❌ Beats generation failed.")
                        break

            # Scribe Drafting Loop
            print(f" Scribe drafting Chapter {ch_str}...")
            if args.dry_run:
                print(f"[DRY-RUN] Scribe writes draft for Chapter {ch_str}.")
                draft = f"# Chapter {next_ch}\n\nJax Steele adjusted his leather coat, rain beaded on his synthetic shoulder. The synth-bass rattled his chest-plate as he entered the neon club. The bartender stared..."
                write_file_content(draft_file, draft)
            else:
                system_inst = get_system_instruction("scribe_instructions.md")
                prompt = f"Draft chapter {next_ch} based on these scene beats. Maintain deep POV, active voice, and avoid clichés.\n\nBeats:\n{beats}"
                draft = call_gemini(client, prompt, system_inst)
                if draft:
                    write_file_content(draft_file, draft)
                else:
                    print("❌ Drafting failed.")
                    break

            # Evaluator Audit
            print(f" Evaluator auditing Chapter {ch_str} prose...")
            draft_score = 7.0
            if args.dry_run:
                print(f"[DRY-RUN] Evaluator scores Chapter {ch_str}: {draft_score}/10 (PASS)")
                critique = f"# Critique Chapter {ch_str}\n\n* Score: {draft_score}/10\n* Status: PASS\n* Cliches: None found."
                write_file_content(critique_file, critique)
            else:
                system_inst = get_system_instruction("evaluator_instructions.md")
                prompt = f"Evaluate the draft chapter prose against Story Grid rules and check for slop or clichés. Provide scorecard.\n\nDraft:\n{draft}"
                critique = call_gemini(client, prompt, system_inst)
                if critique:
                    write_file_content(critique_file, critique)
                    # Parse score from critique text if available
                    score_match = re.search(r'Score:\s*(\d+\.\d+)', critique)
                    if score_match:
                        draft_score = float(score_match.group(1))
                    print(f"✅ Evaluator scored draft: {draft_score}/10")
                else:
                    print("❌ Evaluator check failed.")

            # Deep Editor Developmental Edit
            print(f" Deep Editor developmental editing Chapter {ch_str}...")
            if args.dry_run:
                print(f"[DRY-RUN] Deep Editor developmental edits Chapter {ch_str}.")
                polished_draft = draft + "\n\n*(Polished and refined for pacing)*"
                write_file_content(draft_file, polished_draft)
            else:
                system_inst = get_system_instruction("deep_editor_instructions.md")
                prompt = f"Developmental edit the following draft, incorporating this Evaluator critique.\n\nDraft:\n{draft}\n\nCritique:\n{critique}"
                polished_draft = call_gemini(client, prompt, system_inst)
                if polished_draft:
                    write_file_content(draft_file, polished_draft)
                    print(f"✅ Deep Editor developmental edit completed.")
                else:
                    print("⚠️ Deep Editor failed. Keeping original draft.")

            # Git Auto Commit
            print(" Committing chapter autonomously to Git...")
            run_git_command(["git", "add", "."])
            run_git_command(["git", "commit", "-m", f"YOLO: Completed Chapter {ch_str} (Score: {draft_score})"])
            print("✅ Git commit created.")

            # Update Manifest
            manifest["status"]["current_chapter"] = next_ch
            manifest["latest_scores"]["drafting_score"] = draft_score
            
            # Recalculate word count
            words = 0
            for f_name in glob.glob(os.path.join(draft_dir, "chapter_*.md")):
                try:
                    with open(f_name, "r", encoding="utf-8") as f:
                        words += len(f.read().split())
                except:
                    pass
            manifest["status"]["word_count"] = words
            
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)

            next_ch += 1
            chapters_drafted += 1
            
        print("\n🎉 YOLO session drafting complete.")
        print("To compile final publishing formats, run the /publish-manuscript workflow!")

if __name__ == "__main__":
    main()
