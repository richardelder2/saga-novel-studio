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
    print("\n🎉 SUCCESS! Your new writing desk is ready.")
    print(f"Folder: {new_project_path}")

if __name__ == "__main__":
    main()
