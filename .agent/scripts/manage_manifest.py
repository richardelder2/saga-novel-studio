import os
import sys
import json
import uuid
import datetime
import re
import argparse
import subprocess

def get_git_branch(path):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "main"

def locate_registry(workspace_path):
    paths = [
        # Sibling CoAuthor
        os.path.abspath(os.path.join(os.path.dirname(workspace_path), "CoAuthor", ".agent", "projects_registry.json")),
        # Parent
        os.path.abspath(os.path.join(os.path.dirname(workspace_path), "projects_registry.json")),
        # Local
        os.path.abspath(os.path.join(workspace_path, ".agent", "projects_registry.json")),
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    # Default to sibling CoAuthor if it exists, otherwise local
    sibling_coauthor_dir = os.path.abspath(os.path.join(os.path.dirname(workspace_path), "CoAuthor", ".agent"))
    if os.path.isdir(sibling_coauthor_dir):
        return os.path.join(sibling_coauthor_dir, "projects_registry.json")
    return os.path.join(workspace_path, ".agent", "projects_registry.json")

def load_registry(registry_path):
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_registry(registry_path, registry_data):
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving registry: {e}")
        return False

def scan_projects(workspace_path, registry_path):
    projects = {}
    
    # 1. Load from registry first
    registry = load_registry(registry_path)
    for p in registry:
        path = p.get("path")
        if path and os.path.isdir(path):
            manifest_path = os.path.join(path, "00_Story_Bible", "project_manifest.json")
            if os.path.exists(manifest_path):
                projects[os.path.abspath(path)] = os.path.abspath(manifest_path)

    # 2. Dynamically scan parent directory siblings
    parent_dir = os.path.dirname(workspace_path)
    if os.path.isdir(parent_dir):
        for item in os.listdir(parent_dir):
            item_path = os.path.join(parent_dir, item)
            if os.path.isdir(item_path):
                manifest_path = os.path.join(item_path, "00_Story_Bible", "project_manifest.json")
                if os.path.exists(manifest_path):
                    projects[os.path.abspath(item_path)] = os.path.abspath(manifest_path)
                    
    # Compile actual manifest details
    project_list = []
    for path, manifest_path in projects.items():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            project_list.append({
                "path": path,
                "manifest": data
            })
        except Exception:
            pass
            
    return project_list

def recalculate_stats(workspace_path):
    drafting_dir = os.path.join(workspace_path, "02_Drafting")
    word_count = 0
    current_chapter = 0
    
    if os.path.isdir(drafting_dir):
        chapter_files = []
        for file in os.listdir(drafting_dir):
            if file.endswith(".md"):
                match = re.search(r'\d+', file)
                if match:
                    chap_num = int(match.group())
                    chapter_files.append((chap_num, file))
                else:
                    chapter_files.append((0, file))
        
        for chap_num, file in chapter_files:
            file_path = os.path.join(drafting_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    words = len(content.split())
                    word_count += words
                    if chap_num > current_chapter:
                        current_chapter = chap_num
            except Exception:
                pass
                
        if current_chapter == 0 and len(chapter_files) > 0:
            current_chapter = len(chapter_files)
            
    return word_count, current_chapter

def print_dashboard(project_list, current_path):
    print("\n" + "=" * 80)
    print(" " * 22 + "📖 THE NOVEL FACTORY DIRECTORY 📖")
    print("=" * 80)
    print(f"{'Title':<22} | {'Phase':<17} | {'Chap':<4} | {'Words':<6} | {'Critic':<6} | {'Git Branch':<10} {'Status'}")
    print("-" * 80)
    
    for item in sorted(project_list, key=lambda x: x["manifest"].get("title", "")):
        path = item["path"]
        manifest = item["manifest"]
        
        title = manifest.get("title", "Untitled Book")
        if len(title) > 20:
            title = title[:17] + "..."
            
        status_info = manifest.get("status", {})
        phase = status_info.get("active_phase", "Phase 1: Planning")
        if len(phase) > 15:
            phase = phase[:14] + "..."
            
        chap = status_info.get("current_chapter", 0)
        words = status_info.get("word_count", 0)
        
        scores = manifest.get("latest_scores", {})
        # Get the latest available score
        critic = "N/A"
        for s_type in ["editorial_score", "drafting_score", "foundation_score"]:
            val = scores.get(s_type)
            if val is not None:
                critic = f"{val:.1f}"
                break
                
        branch = manifest.get("git_branch", "main")
        if len(branch) > 9:
            branch = branch[:8] + "..."
            
        is_current = os.path.abspath(path) == os.path.abspath(current_path)
        marker = "⭐ [ACTIVE]" if is_current else ""
        
        print(f"{title:<22} | {phase:<17} | {chap:<4} | {words:<6} | {critic:<6} | {branch:<10} {marker}")
        
    print("=" * 80)
    print(f"Total Projects Tracked: {len(project_list)}")
    print("=" * 80 + "\n")

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Manage project manifests and multi-project registry.")
    subparsers = parser.add_subparsers(dest="command")
    
    # Init manifest
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--genre", default="General Fiction")
    
    # Update manifest
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--phase")
    update_parser.add_argument("--title")
    update_parser.add_argument("--genre")
    update_parser.add_argument("--chapter", type=int)
    update_parser.add_argument("--total-chapters", type=int)
    update_parser.add_argument("--foundation-score", type=float)
    update_parser.add_argument("--drafting-score", type=float)
    update_parser.add_argument("--editorial-score", type=float)
    update_parser.add_argument("--recalculate", action="store_true")
    
    # Register project
    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("--path")
    
    # List projects
    subparsers.add_parser("list")
    
    # Read/Show manifest
    subparsers.add_parser("show")
    
    args = parser.parse_args()
    
    workspace_path = os.getcwd()
    manifest_path = os.path.join(workspace_path, "00_Story_Bible", "project_manifest.json")
    registry_path = locate_registry(workspace_path)
    
    if args.command == "init":
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        data = {
            "project_id": str(uuid.uuid4()),
            "title": args.title,
            "genre": args.genre,
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
            "git_branch": get_git_branch(workspace_path),
            "last_updated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Initialized manifest in {manifest_path}")
        
    elif args.command == "update":
        if not os.path.exists(manifest_path):
            print(f"❌ Error: manifest not found at {manifest_path}. Run init first.")
            sys.exit(1)
            
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if args.phase:
            data["status"]["active_phase"] = args.phase
        if args.title:
            data["title"] = args.title
        if args.genre:
            data["genre"] = args.genre
        if args.chapter is not None:
            data["status"]["current_chapter"] = args.chapter
        if args.total_chapters is not None:
            data["status"]["total_chapters"] = args.total_chapters
            
        if args.foundation_score is not None:
            data["latest_scores"]["foundation_score"] = args.foundation_score
        if args.drafting_score is not None:
            data["latest_scores"]["drafting_score"] = args.drafting_score
        if args.editorial_score is not None:
            data["latest_scores"]["editorial_score"] = args.editorial_score
            
        if args.recalculate:
            words, chap = recalculate_stats(workspace_path)
            data["status"]["word_count"] = words
            if chap > 0:
                data["status"]["current_chapter"] = chap
                
        data["git_branch"] = get_git_branch(workspace_path)
        data["last_updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Updated manifest in {manifest_path}")
        
    elif args.command == "register":
        path_to_register = os.path.abspath(args.path if args.path else workspace_path)
        m_path = os.path.join(path_to_register, "00_Story_Bible", "project_manifest.json")
        if not os.path.exists(m_path):
            print(f"❌ Cannot register path '{path_to_register}': manifest not found.")
            sys.exit(1)
            
        with open(m_path, 'r', encoding='utf-8') as f:
            m_data = json.load(f)
            
        registry = load_registry(registry_path)
        
        # Avoid duplicate entry
        updated_registry = [p for p in registry if os.path.abspath(p.get("path", "")) != path_to_register]
        updated_registry.append({
            "project_id": m_data.get("project_id"),
            "title": m_data.get("title"),
            "path": path_to_register,
            "created_at": m_data.get("created_at")
        })
        
        if save_registry(registry_path, updated_registry):
            print(f"✅ Registered project '{m_data.get('title')}' at {path_to_register} inside global registry: {registry_path}")
            
    elif args.command == "list":
        project_list = scan_projects(workspace_path, registry_path)
        print_dashboard(project_list, workspace_path)
        
    elif args.command == "show":
        if not os.path.exists(manifest_path):
            print(f"❌ No manifest found in this directory: {manifest_path}")
            sys.exit(1)
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(json.dumps(data, indent=2))
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
