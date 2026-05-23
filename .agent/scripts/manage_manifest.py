import os
import sys
import json
import uuid
import datetime
import re
import argparse

# Import core utilities
import agent_core

def locate_registry(workspace_path):
    paths = [
        # Script-relative central folder (always reliable for script origin)
        os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "projects_registry.json")),
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
    # Default fallback relative to script
    script_fallback = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "projects_registry.json"))
    if os.path.exists(os.path.dirname(script_fallback)):
        return script_fallback
    # Default to sibling CoAuthor if it exists, otherwise local
    sibling_coauthor_dir = os.path.abspath(os.path.join(os.path.dirname(workspace_path), "CoAuthor", ".agent"))
    if os.path.isdir(sibling_coauthor_dir):
        return os.path.join(sibling_coauthor_dir, "projects_registry.json")
    return os.path.join(workspace_path, ".agent", "projects_registry.json")

def load_registry(registry_path):
    content = agent_core.read_file_content(registry_path)
    if content:
        try:
            return json.loads(content)
        except Exception:
            return []
    return []

def save_registry(registry_path, registry_data):
    try:
        content = json.dumps(registry_data, indent=2)
        return agent_core.write_file_content(registry_path, content)
    except Exception as e:
        print(f"Error preparing registry data: {e}")
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
        content = agent_core.read_file_content(manifest_path)
        if content:
            try:
                data = json.loads(content)
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
            content = agent_core.read_file_content(file_path)
            if content:
                words = len(content.split())
                word_count += words
                if chap_num > current_chapter:
                    current_chapter = chap_num
                
        if current_chapter == 0 and len(chapter_files) > 0:
            current_chapter = len(chapter_files)
            
    return word_count, current_chapter

def print_dashboard(project_list, current_path):
    if sys.platform == 'win32':
        os.system('')

    CYAN = "\033[36m"
    B_CYAN = "\033[96m"
    B_BLUE = "\033[94m"
    B_MAGENTA = "\033[95m"
    GREEN = "\033[32m"
    B_GREEN = "\033[92m"
    YELLOW = "\033[33m"
    WHITE = "\033[37m"
    B_WHITE = "\033[97m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(f"\n{BOLD}{B_MAGENTA}┌────────────────────────┬──────────────────┬──────┬────────┬────────┬─────────────┐{RESET}")
    print(f"{BOLD}{B_MAGENTA}│{RESET}                       {BOLD}{B_WHITE}📖 THE NOVEL FACTORY DIRECTORY 📖{RESET}                      {BOLD}{B_MAGENTA}│{RESET}")
    print(f"{BOLD}{B_MAGENTA}├────────────────────────┼──────────────────┼──────┼────────┼────────┼─────────────┤{RESET}")
    print(f"{BOLD}{B_MAGENTA}│{RESET} {BOLD}{B_CYAN}{'Title':<22}{RESET} {BOLD}{B_MAGENTA}│{RESET} {BOLD}{B_CYAN}{'Phase':<16}{RESET} {BOLD}{B_MAGENTA}│{RESET} {BOLD}{B_CYAN}{'Chap':<4}{RESET} {BOLD}{B_MAGENTA}│{RESET} {BOLD}{B_CYAN}{'Words':<6}{RESET} {BOLD}{B_MAGENTA}│{RESET} {BOLD}{B_CYAN}{'Critic':<6}{RESET} {BOLD}{B_MAGENTA}│{RESET} {BOLD}{B_CYAN}{'Git Branch':<11}{RESET} {BOLD}{B_MAGENTA}│{RESET}")
    print(f"{BOLD}{B_MAGENTA}├────────────────────────┼──────────────────┼──────┼────────┼────────┼─────────────┤{RESET}")
    
    for item in sorted(project_list, key=lambda x: x["manifest"].get("title", "")):
        path = item["path"]
        manifest = item["manifest"]
        
        title = manifest.get("title", "Untitled Book")
        if len(title) > 22:
            title = title[:19] + "..."
            
        status_info = manifest.get("status", {})
        phase = status_info.get("active_phase", "Planning")
        if len(phase) > 16:
            phase = phase[:13] + "..."
            
        chap = status_info.get("current_chapter", 0)
        words = status_info.get("word_count", 0)
        
        scores = manifest.get("latest_scores", {})
        critic = "N/A"
        for s_type in ["editorial_score", "drafting_score", "foundation_score"]:
            val = scores.get(s_type)
            if val is not None:
                critic = f"{val:.1f}"
                break
                
        branch = manifest.get("git_branch", "main")
        if len(branch) > 11:
            branch = branch[:8] + "..."
            
        is_current = os.path.abspath(path) == os.path.abspath(current_path)
        
        if is_current:
            title_styled = f"{BOLD}{B_GREEN}{title:<22}{RESET}"
            phase_styled = f"{B_GREEN}{phase:<16}{RESET}"
            chap_styled = f"{B_GREEN}{chap:<4}{RESET}"
            words_styled = f"{B_GREEN}{words:<6,}{RESET}"
            critic_styled = f"{B_GREEN}{critic:<6}{RESET}"
            branch_styled = f"{B_GREEN}{branch:<11}{RESET}"
            row_marker = f" {BOLD}{B_GREEN}⭐ [ACTIVE]{RESET}"
        else:
            title_styled = f"{WHITE}{title:<22}{RESET}"
            phase_styled = f"{GRAY}{phase:<16}{RESET}"
            chap_styled = f"{WHITE}{chap:<4}{RESET}"
            words_styled = f"{WHITE}{words:<6,}{RESET}"
            critic_styled = f"{YELLOW}{critic:<6}{RESET}"
            branch_styled = f"{GRAY}{branch:<11}{RESET}"
            row_marker = ""
            
        print(f"{BOLD}{B_MAGENTA}│{RESET} {title_styled} {BOLD}{B_MAGENTA}│{RESET} {phase_styled} {BOLD}{B_MAGENTA}│{RESET} {chap_styled} {BOLD}{B_MAGENTA}│{RESET} {words_styled} {BOLD}{B_MAGENTA}│{RESET} {critic_styled} {BOLD}{B_MAGENTA}│{RESET} {branch_styled} {BOLD}{B_MAGENTA}│{RESET}{row_marker}")
        
    print(f"{BOLD}{B_MAGENTA}└────────────────────────┴──────────────────┴──────┴────────┴────────┴─────────────┘{RESET}")
    print(f" {BOLD}{WHITE}Total Projects Tracked:{RESET} {B_CYAN}{len(project_list)}{RESET}\n")

def main():
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
            "git_branch": agent_core.run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or "main",
            "last_updated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        agent_core.write_file_content(manifest_path, json.dumps(data, indent=2))
        print(f"✅ Initialized manifest in {manifest_path}")
        
    elif args.command == "update":
        content = agent_core.read_file_content(manifest_path)
        if not content:
            print(f"❌ Error: manifest not found or empty at {manifest_path}. Run init first.")
            sys.exit(1)
            
        try:
            data = json.loads(content)
        except Exception as e:
            print(f"❌ Error decoding manifest JSON: {e}")
            sys.exit(1)
            
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
                
        data["git_branch"] = agent_core.run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or "main"
        data["last_updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        
        agent_core.write_file_content(manifest_path, json.dumps(data, indent=2))
        print(f"✅ Updated manifest in {manifest_path}")
        
    elif args.command == "register":
        path_to_register = os.path.abspath(args.path if args.path else workspace_path)
        m_path = os.path.join(path_to_register, "00_Story_Bible", "project_manifest.json")
        
        m_content = agent_core.read_file_content(m_path)
        if not m_content:
            print(f"❌ Cannot register path '{path_to_register}': manifest not found or empty.")
            sys.exit(1)
            
        try:
            m_data = json.loads(m_content)
        except Exception as e:
            print(f"❌ Error decoding project manifest: {e}")
            sys.exit(1)
            
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
        content = agent_core.read_file_content(manifest_path)
        if not content:
            print(f"❌ No manifest found in this directory: {manifest_path}")
            sys.exit(1)
        print(content)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
