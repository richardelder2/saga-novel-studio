import os
import shutil
import random
import subprocess
import sys

# Cool names generator
ADJECTIVES = ["crimson", "obsidian", "nebular", "astral", "midnight", "solar", "lunar", "silent", "phantom", "echoing", "crystal", "iron", "velvet", "storm", "cyber", "ethereal"]
NOUNS = ["void", "nexus", "peak", "spire", "drift", "engine", "protocol", "odyssey", "whisper", "horizon", "sanctuary", "citadel", "forge", "archive", "expanse"]

def generate_name():
    return f"{random.choice(ADJECTIVES)}-{random.choice(NOUNS)}"

import argparse
import sys
import os
import shutil
import subprocess
import random

# Cool names generator
ADJECTIVES = ["crimson", "obsidian", "nebular", "astral", "midnight", "solar", "lunar", "silent", "phantom", "echoing", "crystal", "iron", "velvet", "storm", "cyber", "ethereal"]
NOUNS = ["void", "nexus", "peak", "spire", "drift", "engine", "protocol", "odyssey", "whisper", "horizon", "sanctuary", "citadel", "forge", "archive", "expanse"]

def generate_name():
    return f"{random.choice(ADJECTIVES)}-{random.choice(NOUNS)}"

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Start a new book project.")
    parser.add_argument("--name", type=str, help="Name of the new project")
    parser.add_argument("--generate", action="store_true", help="Generate a random name")
    parser.add_argument("--mode", type=str, choices=["manual", "yolo"], default=None, help="Writing mode choice (manual or yolo)")
    args = parser.parse_args()

    print("✨ WELCOME TO THE NOVEL FACTORY ✨")
    print("-----------------------------------")
    
    # 1. Get Project Name
    project_name = ""
    if args.name:
        project_name = args.name
    else:
        # Default to generation if no name provided or --generate flag used
        project_name = generate_name()
    
    # 1.5. Get Development Mode
    mode_choice = "manual"
    if args.mode:
        mode_choice = args.mode
    else:
        # Prompt only if in an interactive terminal
        if sys.stdin.isatty():
            try:
                print("\nSelect Book Development Mode:")
                print("  1. 💻 MANUAL MODE (Collaborative Chapter-by-Chapter) [Default]")
                print("  2. 🚀 YOLO MODE (Autonomous End-to-End Novel Generation)")
                choice = input("Enter choice (1 or 2): ").strip()
                if choice == "2":
                    mode_choice = "yolo"
            except Exception:
                mode_choice = "manual"
        else:
            mode_choice = "manual"
            
    print(f"\nConfiguration: Name = '{project_name}', Mode = '{mode_choice.upper()}'")
    
    # 2. Determine Paths
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    new_project_path = os.path.join(parent_dir, project_name)
    
    if os.path.exists(new_project_path):
        print(f"❌ Error: A folder named '{project_name}' already exists in {parent_dir}")
        return

    print(f"\n🚀 Creating new book project: {project_name}...")
    print(f"📍 Location: {new_project_path}")
    
    # 3. Copy Files
    ignore_patterns = shutil.ignore_patterns(".git", ".git/*", "__pycache__", "*.pyc", "start_new_book.py", "extracted_text.txt")
    
    try:
        shutil.copytree(current_dir, new_project_path, ignore=ignore_patterns)
        print("✅ Files copied successfully.")
    except Exception as e:
        print(f"❌ Error copying files: {e}")
        return

    # 3.5. Update and Register Manifest
    try:
        import uuid
        import json
        import datetime
        
        manifest_path = os.path.join(new_project_path, "00_Story_Bible", "project_manifest.json")
        new_uuid = str(uuid.uuid4())
        
        # Determine clean Title from project folder name
        title = project_name.replace("-", " ").replace("_", " ").title()
        
        manifest_data = {
            "project_id": new_uuid,
            "title": title,
            "genre": "General Fiction", # Will be updated during kickoff
            "created_at": datetime.date.today().isoformat(),
            "status": {
                "active_phase": "Phase 1: Planning",
                "current_chapter": 0,
                "total_chapters": 0,
                "word_count": 0
            },
            "latest_scores": {
                "foundation_score": None,
                "drafting_score": None,
                "editorial_score": None
            },
            "mode": mode_choice,
            "git_branch": "main",
            "last_updated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)
            
        print("📝 Local project manifest generated.")
        
        # Register new book in the template's registry
        script_path = os.path.join(current_dir, ".agent", "scripts", "manage_manifest.py")
        if os.path.exists(script_path):
            subprocess.run([sys.executable, script_path, "register", "--path", new_project_path], cwd=current_dir, check=True)
            print("📋 Registered project in central repository registry.")
            
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize manifest or register project: {e}")

    # 4. Initialize Git
    try:
        print("🔧 Initializing clean version control...")
        subprocess.run(["git", "init"], cwd=new_project_path, check=True)
        subprocess.run(["git", "add", "."], cwd=new_project_path, check=True)
        try:
            subprocess.run(["git", "commit", "-m", "Initial commit from Novel Factory"], cwd=new_project_path, check=False)
        except:
            pass
        print("✅ Git repository created.")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize Git: {e}")

    # 5. Done
    if sys.platform == 'win32':
        os.system('')
        
    B_CYAN = "\033[96m"
    B_GREEN = "\033[92m"
    B_WHITE = "\033[97m"
    YELLOW = "\033[33m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(f"\n{BOLD}{B_CYAN}┌──────────────────────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{B_CYAN}│{RESET}  {BOLD}{B_GREEN}🎉 SUCCESS! YOUR NEW WRITING DESK IS READY!{RESET:<66}  {BOLD}{B_CYAN}│{RESET}")
    print(f"{BOLD}{B_CYAN}├──────────────────────────────────────────────────────────────────────────────┤{RESET}")
    print(f"{BOLD}{B_CYAN}│{RESET}  Desk created successfully at:                                                {BOLD}{B_CYAN}│{RESET}")
    display_path = new_project_path
    if len(display_path) > 72:
        display_path = "..." + display_path[-69:]
    print(f"{BOLD}{B_CYAN}│{RESET}  {GRAY}{display_path:<74}{RESET}  {BOLD}{B_CYAN}│{RESET}")
    print(f"{BOLD}{B_CYAN}├──────────────────────────────────────────────────────────────────────────────┤{RESET}")
    
    if mode_choice == "yolo":
        print(f"{BOLD}{B_CYAN}│{RESET}  {BOLD}{B_CYAN}🚀 YOLO MODE IS CONFIGURED!{RESET:<74}  {BOLD}{B_CYAN}│{RESET}")
        print(f"{BOLD}{B_CYAN}│{RESET}  To launch the autonomous writer engine:                                      {BOLD}{B_CYAN}│{RESET}")
        print(f"{BOLD}{B_CYAN}│{RESET}    {BOLD}{YELLOW}cd {project_name}{RESET:<70}  {BOLD}{B_CYAN}│{RESET}")
        print(f"{BOLD}{B_CYAN}│{RESET}    {BOLD}{YELLOW}saga --yolo{RESET:<70}  {BOLD}{B_CYAN}│{RESET}")
    else:
        print(f"{BOLD}{B_CYAN}│{RESET}  To begin collaborative manual drafting:                                      {BOLD}{B_CYAN}│{RESET}")
        print(f"{BOLD}{B_CYAN}│{RESET}    {BOLD}{YELLOW}cd {project_name}{RESET:<70}  {BOLD}{B_CYAN}│{RESET}")
        print(f"{BOLD}{B_CYAN}│{RESET}    {BOLD}{YELLOW}saga --status{RESET:<70}  {BOLD}{B_CYAN}│{RESET}")
        
    print(f"{BOLD}{B_CYAN}└──────────────────────────────────────────────────────────────────────────────┘{RESET}\n")

if __name__ == "__main__":
    main()

