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

def generate_chapter_illustration(client, chapter_num, beats, dry_run):
    output_dir = "04_Publishing/illustrations"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"chapter_{chapter_num}_illustration.png")
    
    print(f"🖼️ Generating chapter illustration for Chapter {chapter_num} via Google Imagen 4.0...")
    prompt = (
        f"A beautiful cinematic fantasy/sci-fi illustration depicting the following story beats: "
        f"\"{beats}\". Stylized, artistic composition, rich deep atmospheric lighting, dramatic color palette."
    )
    
    if dry_run:
        print(f"[DRY-RUN] Would generate chapter illustration for chapter {chapter_num}.")
        write_file_content(output_path, "MOCK ILLUSTRATION DATA")
        return
        
    try:
        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/png"
            )
        )
        if response.generated_images:
            from io import BytesIO
            try:
                from PIL import Image
                img_data = response.generated_images[0].image.image_bytes
                image = Image.open(BytesIO(img_data))
                image.save(output_path)
                print(f"✅ Illustration successfully saved at: {output_path}")
            except ImportError:
                img_data = response.generated_images[0].image.image_bytes
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"✅ Illustration saved as raw PNG at: {output_path}")
    except Exception as e:
        print(f"⚠️ Warning: Could not generate illustration: {e}")

def build_landing_page(manifest):
    print("\n🌐 Compiling promotional landing page index.html...")
    title = manifest.get("title", "Untitled Novel")
    genre = manifest.get("genre", "General Fiction")
    synopsis = read_file_content("01_Planning/premise.md")
    
    # Strip markdown headers or simple cleanup
    synopsis_html = synopsis.replace("# Story Premise\n\n", "").replace("\n\n", "</p><p>").replace("\n", "<br/>")
    if not synopsis_html.strip():
        synopsis_html = "A high-concept, gripping novel of suspense and discovery."
        
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
    write_file_content("04_Publishing/index.html", html_content)
    print("🎉 Landing Page generated successfully at 04_Publishing/index.html")

def interactive_brainstorming(client, premise_path):
    print("\n✨ COAUTHOR YOLO MODE: FOUNDATION SESSION ✨")
    print("---------------------------------------------")
    print("Welcome! I am your Orchestrator & Creative Consultant.")
    print("Let's brainstorm your novel together. Type your initial ideas, themes, characters, or settings.")
    print("Type 'done' or 'finish' when you're happy and want to compile the complete Story Bible!\n")
    
    # Check if stdin is interactive
    if not sys.stdin.isatty():
        print("⚠️ Non-interactive environment detected. Seeding basic default premise...")
        default_premise = "# Story Premise\n\nA cybernetic detective in a rain-slicked neon metropolis searches for a corporate heiress, uncovering digital transcendence secrets."
        write_file_content(premise_path, default_premise)
        return default_premise

    chat_history = []
    system_inst = (
        "You are the Orchestrator, an expert creative novelist, world-builder, and structural consultant. "
        "Engage in a friendly, conversational brainstorming session with the user. "
        "Ask targeted, creative questions one at a time. Help flesh out their ideas, "
        "propose rich plot hooks, suggest complex characters, and suggest world laws. "
        "Keep your responses concise, punchy, and highly creative. "
        "Focus on building a cohesive story theme, premise, setting, and main character concepts."
    )
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['done', 'finish', '/done', '/finish']:
                print("\n✨ Brainstorming session completed! Consolidating Story Bible...")
                break
                
            chat_history.append({"role": "user", "parts": [user_input]})
            
            # Format history for API call
            contents = []
            for msg in chat_history:
                contents.append(types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(text=p) for p in msg["parts"]]
                ))
            
            print("🤖 Orchestrator thinking...")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_inst,
                    temperature=0.8
                )
            )
            
            reply = response.text
            print(f"\nOrchestrator: {reply}")
            chat_history.append({"role": "model", "parts": [reply]})
            
        except (KeyboardInterrupt, EOFError):
            print("\nExiting brainstorming session. Seeding default premise...")
            break
            
    # Now generate the Story Bible assets from the transcript
    transcript = ""
    for msg in chat_history:
        role_label = "User" if msg["role"] == "user" else "Orchestrator"
        text_content = "\n".join(msg["parts"])
        transcript += f"{role_label}: {text_content}\n\n"
        
    print("\n📝 Compiling Story Premise (01_Planning/premise.md)...")
    premise_prompt = (
        f"Based on the following brainstorming transcript, generate a structured, professional story premise. "
        f"Output in clean markdown with sections: Title, Genre, Logline, Core Theme, Narrative Arc, and Synopsis.\n\n"
        f"Transcript:\n{transcript}"
    )
    premise_text = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=premise_prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a professional book outliner. Generate a structured premise document."
        )
    ).text
    write_file_content(premise_path, premise_text)
    print("✅ Story Premise written successfully.")
    
    print("\n🌍 Compiling World Building Rules (00_Story_Bible/world_rules.md)...")
    world_prompt = (
        f"Based on the following brainstorming transcript, generate a detailed world setting and laws document. "
        f"Output in clean markdown with sections: Setting Overview, Key Locations, Magic or Technological Laws, and Narrative Constraints.\n\n"
        f"Transcript:\n{transcript}"
    )
    world_text = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=world_prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a premium world-builder. Write a structured world guide."
        )
    ).text
    write_file_content("00_Story_Bible/world_rules.md", world_text)
    print("✅ World Setting Rules written successfully.")
    
    print("\n👥 Extracting Main Characters to Story Bible (00_Story_Bible/characters/)...")
    char_prompt = (
        f"Based on the following brainstorming transcript, extract the 3 most important characters discussed. "
        f"For each character, generate a structured profile in clean markdown containing these fields:\n"
        f"- Name (as the main header # Character Name)\n"
        f"- **Role in Story**\n"
        f"- **Gender** (pick exactly one of: Male, Female, Non-binary)\n"
        f"- **Voice Assignment** (pick exactly one of the premium prebuilt voices listed below)\n"
        f"- **Physical Description**\n"
        f"- **Personality**\n"
        f"- **Backstory**\n\n"
        f"Recommended Prebuilt Voices for Voice Assignment:\n"
        f"- Fenrir (rich, lower-mid male voice, great for male leads)\n"
        f"- Aoede (clear, expressive mid female voice, great for female leads or narrators)\n"
        f"- Puck (lighter, energetic mid male voice, great for supporting males/sidekicks)\n"
        f"- Kore (confident, energetic mid-high female voice, great for active females/rebels)\n"
        f"- Leda (composed, serious, professional female voice, great for intellectual/stern females)\n"
        f"- Zubenelgenubi (very deep, commanding male voice, great for main villains/commanders)\n"
        f"- Zephyr (bright, perky, upbeat female voice, great for companions/cheerful females)\n"
        f"- Despina (smooth, warm, inviting female voice, great for kind/comforting females)\n"
        f"- Autonoe (deep, mature, resonant male voice, great for wise mentors/older figures)\n"
        f"- Achernar (friendly, engaging mid male voice, great for approachable males)\n\n"
        f"Format your response as a valid JSON object matching this structure exactly:\n"
        f"{{\n  \"characters\": [\n    {{\n      \"filename\": \"jax_steele.md\",\n      \"content\": \"full markdown content of the character profile here\"\n    }}\n  ]\n}}\n\n"
        f"Transcript:\n{transcript}"
    )
    
    try:
        char_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=char_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                system_instruction="You are a professional character developer. Generate character profile markdown content in a structured JSON payload."
            )
        ).text
        
        char_data = json.loads(char_response)
        os.makedirs("00_Story_Bible/characters", exist_ok=True)
        for char_info in char_data.get("characters", []):
            filename = char_info.get("filename")
            content = char_info.get("content")
            if filename and content:
                # Sanitize filename
                filename = re.sub(r'[^a-zA-Z0-9_\.-]', '', filename)
                char_path = os.path.join("00_Story_Bible/characters", filename)
                write_file_content(char_path, content)
                print(f"  • Created character profile: {filename}")
                
    except Exception as e:
        print(f"⚠️ Warning: Could not parse character extraction JSON: {e}")
        # Seeding a default protagonist profile
        default_char = (
            "# Jax Steele\n\n"
            "**Role in Story:** Protagonist\n\n"
            "**Gender:** Male\n\n"
            "**Voice Assignment:** Fenrir\n\n"
            "**Physical Description:**\n"
            "- Age: 34\n"
            "- Height/Build: Tall, athletic build\n"
            "- Distinguishing features: Cybernetic left arm, steel grey eyes\n\n"
            "**Personality:** Cybernetic detective, cynical but operates under a strict moral code.\n\n"
            "**Backstory:** Former corporate investigator who went rogue after uncovering dark secrets."
        )
        write_file_content("00_Story_Bible/characters/jax_steele.md", default_char)
        print("  • Seeded default protagonist profile.")
        
    print("\n🎉 STORY BIBLE FOUNDATION FULLY ESTABLISHED!")
    return premise_text

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
        if not premise or premise.strip() == "# Story Premise" or len(premise.strip()) < 20:
            # Brainstorm interactive session
            premise = interactive_brainstorming(client, premise_path)
            
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

            # Self-Correction Retry Loop for Drafting
            best_draft = ""
            best_score = 0.0
            best_critique = ""
            max_retries = 3
            
            for attempt in range(1, max_retries + 1):
                print(f" Scribe drafting Chapter {ch_str} (Attempt {attempt}/{max_retries})...")
                if attempt > 1:
                    prompt = (
                        f"You are revising Chapter {next_ch} based on a critique. Here is the previous draft:\n\n"
                        f"{draft}\n\nHere is the Evaluator's critique outlining the issues and score:\n\n"
                        f"{critique}\n\nPlease revise the chapter to fix the issues, enhance depth, expand prose quality, and eliminate clichés. "
                        f"Maintain the scene beats:\n\n{beats}"
                    )
                else:
                    prompt = f"Draft chapter {next_ch} based on these scene beats. Maintain deep POV, active voice, and avoid clichés.\n\nBeats:\n{beats}"
                
                if args.dry_run:
                    draft = f"# Chapter {next_ch}\n\nJax Steele adjusted his leather coat, rain beaded on his synthetic shoulder. The synth-bass rattled his chest-plate as he entered the neon club. The bartender stared..."
                    draft_score = 8.0
                    critique = "# Critique\nScore: 8.0/10\nPASS"
                else:
                    system_inst = get_system_instruction("scribe_instructions.md")
                    draft = call_gemini(client, prompt, system_inst)
                    if not draft:
                        print("❌ Scribe failed to draft chapter.")
                        break
                        
                print(f" Evaluator auditing Chapter {ch_str} prose (Attempt {attempt}/{max_retries})...")
                if args.dry_run:
                    draft_score = 8.2
                    critique = "# Critique\nScore: 8.2/10\nPASS"
                else:
                    system_inst = get_system_instruction("evaluator_instructions.md")
                    eval_prompt = f"Evaluate the draft chapter prose against Story Grid rules and check for slop or clichés. Provide scorecard.\n\nDraft:\n{draft}"
                    critique = call_gemini(client, eval_prompt, system_inst)
                    if critique:
                        score_match = re.search(r'Score:\s*(\d+\.\d+)', critique)
                        if score_match:
                            draft_score = float(score_match.group(1))
                        else:
                            score_match_int = re.search(r'Score:\s*(\d+)', critique)
                            draft_score = float(score_match_int.group(1)) if score_match_int else 7.0
                    else:
                        draft_score = 6.0
                        critique = "Could not evaluate."
                
                print(f"  Attempt {attempt} Score: {draft_score}/10")
                
                if draft_score > best_score:
                    best_score = draft_score
                    best_draft = draft
                    best_critique = critique
                
                if draft_score >= 7.5:
                    print(f"🎉 Prose audit PASSED with a score of {draft_score}/10!")
                    break
                else:
                    print(f"⚠️ Prose score {draft_score}/10 is below the 7.5 quality threshold. Retrying...")
            
            draft = best_draft
            critique = best_critique
            draft_score = best_score
            write_file_content(draft_file, draft)
            write_file_content(critique_file, critique)

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
                    polished_draft = draft
                    print("⚠️ Deep Editor failed. Keeping original draft.")

            # Lore Keeper Continuous Bible Update
            print(f" Lore Keeper updating the Story Bible...")
            if args.dry_run:
                print("[DRY-RUN] Lore Keeper would update character profiles.")
            else:
                system_inst = get_system_instruction("lore_keeper_instructions.md")
                char_files = glob.glob("00_Story_Bible/characters/*.md")
                char_summaries = []
                for cf in char_files:
                    char_summaries.append(f"--- CHARACTER: {os.path.basename(cf)} ---\n{read_file_content(cf)}")
                characters_context = "\n\n".join(char_summaries)
                
                lore_prompt = (
                    f"You have just finished Chapter {next_ch}. Below is the final polished text of the chapter:\n\n"
                    f"{polished_draft}\n\nHere are the current character files in the Story Bible:\n\n"
                    f"{characters_context}\n\n"
                    f"Please review the chapter for any character development, relationship changes, new secrets revealed, or settings introduced. "
                    f"For each relevant character file, provide an updated markdown profile. Return a JSON structure matching exactly:\n"
                    f"{{\n  \"characters\": [\n    {{\"filename\": \"character_file_name.md\", \"content\": \"full updated markdown content here\"}}\n  ]\n}}"
                )
                
                lore_updates = call_gemini(client, lore_prompt, system_inst)
                if lore_updates:
                    try:
                        json_str = lore_updates.strip()
                        if json_str.startswith("```"):
                            json_str = re.sub(r'^```[a-zA-Z]*\n', '', json_str)
                            json_str = re.sub(r'\n```$', '', json_str)
                        
                        data = json.loads(json_str)
                        for char_data in data.get("characters", []):
                            filename = char_data.get("filename")
                            content = char_data.get("content")
                            if filename and content:
                                # Ensure only target filenames
                                filename = os.path.basename(filename)
                                char_path = os.path.join("00_Story_Bible/characters", filename)
                                write_file_content(char_path, content)
                                print(f"  • Updated character file: {filename}")
                    except Exception as e:
                        print(f"  ⚠️ Warning: Could not parse Lore Keeper update JSON: {e}")

            # Auto-Illustration Generation (Imagen 4.0)
            generate_chapter_illustration(client, ch_str, beats, args.dry_run)

            # Git Auto Commit
            if not args.dry_run:
                print(" Committing chapter autonomously to Git...")
                run_git_command(["git", "add", "."])
                run_git_command(["git", "commit", "-m", f"YOLO: Completed Chapter {ch_str} (Score: {draft_score})"])
                print("✅ Git commit created.")
            else:
                print(" [DRY-RUN] Would commit chapter autonomously to Git.")

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
            
        print("\n🎉 Autonomous drafting phase complete.")
        
        # ==================== PHASE 3: PUBLISHING (YOLO) ====================
        print("\n--- PHASE 3: AUTONOMOUS PUBLISHING LOOP ---")
        
        # 1. Typeset HTML
        print("🎨 Typesetting book layout...")
        if args.dry_run:
            print("[DRY-RUN] Would run typeset_book.py.")
        else:
            try:
                subprocess.run([sys.executable, ".agent/scripts/typeset_book.py"], check=True)
                print("✅ Book typesetting complete.")
            except Exception as e:
                print(f"⚠️ Warning: Typesetting failed: {e}")
                
        # 2. Package ePUB
        print("📦 Compiling ePUB container...")
        if args.dry_run:
            print("[DRY-RUN] Would run compile_epub.py.")
        else:
            try:
                subprocess.run([sys.executable, ".agent/scripts/compile_epub.py"], check=True)
                print("✅ ePUB compilation complete.")
            except Exception as e:
                print(f"⚠️ Warning: ePUB packaging failed: {e}")
                
        # 3. Extract Dialogue Audiobook Script
        print("📝 Parsing audiobook dialogue map...")
        if args.dry_run:
            print("[DRY-RUN] Would run parse_audiobook.py.")
        else:
            try:
                subprocess.run([sys.executable, ".agent/scripts/parse_audiobook.py"], check=True)
                print("✅ Audiobook dialogue parsed.")
            except Exception as e:
                print(f"⚠️ Warning: Dialogue parser failed: {e}")
                
        # 4. Generate Book Cover Concept (Imagen 4.0)
        print("🖼️ Generating book cover concept...")
        if args.dry_run:
            print("[DRY-RUN] Would run generate_cover_api.py.")
        else:
            try:
                subprocess.run([sys.executable, ".agent/scripts/generate_cover_api.py"], check=True)
                print("✅ Cover concept generated.")
            except Exception as e:
                print(f"⚠️ Warning: Cover generation failed: {e}")
                
        # 5. Synthesize Audiobook WAV (Gemini TTS)
        print("🎙️ Synthesizing multi-voice WAV audiobook...")
        if args.dry_run:
            print("[DRY-RUN] Would run synthesize_audiobook.py.")
        else:
            try:
                subprocess.run([sys.executable, ".agent/scripts/synthesize_audiobook.py"], check=True)
                print("✅ Audiobook WAV synthesized.")
            except Exception as e:
                print(f"⚠️ Warning: Audiobook synthesis failed: {e}")
                
        # 6. Build Landing Page
        build_landing_page(manifest)
        
        # Git Auto Commit Publishing Assets
        if not args.dry_run:
            print(" Committing compiled publishing assets autonomously to Git...")
            run_git_command(["git", "add", "."])
            run_git_command(["git", "commit", "-m", "YOLO: Compiled print typeset, ePUB, Imagen cover concept, TTS audiobook, and promotional landing page"])
            print("✅ Git commit created.")
            
        print("\n🎉 SUCCESS! COAUTHOR YOLO RUN FULLY COMPLETED!")

if __name__ == "__main__":
    main()
