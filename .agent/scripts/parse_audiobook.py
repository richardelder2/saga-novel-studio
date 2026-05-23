import os
import glob
import re
import csv
import json

def get_character_metadata():
    """
    Scans character profiles to build a directory of characters, their genders, and aliases.
    """
    char_map = {}
    char_dir = "00_Story_Bible/characters"
    
    if os.path.exists(char_dir):
        for file in os.listdir(char_dir):
            if file.endswith(".md"):
                char_key = os.path.splitext(file)[0]
                char_name = char_key.replace("_", " ").title()
                
                path = os.path.join(char_dir, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception:
                    content = ""
                
                # Detect Gender
                gender = "unknown"
                gender_match = re.search(r'gender\s*\**\s*:\s*\**\s*([a-zA-Z]+)', content, re.IGNORECASE)
                if gender_match:
                    gender = gender_match.group(1).strip().lower()
                else:
                    # Heuristic pronoun count
                    content_lower = content.lower()
                    she_count = len(re.findall(r'\bshe\b|\bher\b', content_lower))
                    he_count = len(re.findall(r'\bhe\b|\bhim\b|\bhis\b', content_lower))
                    if she_count > he_count + 2:
                        gender = "female"
                    elif he_count > she_count + 2:
                        gender = "male"
                
                # Detect Aliases / First name
                aliases = [char_name.lower()]
                first_name = char_name.split()[0].lower()
                if first_name not in aliases:
                    aliases.append(first_name)
                
                char_map[char_name] = {
                    "gender": gender,
                    "aliases": aliases
                }
                
    return char_map

def parse_dialogue_from_chapter(filename, idx, char_metadata):
    script_rows = []
    
    with open(filename, "r", encoding="utf-8") as infile:
        content = infile.read()
        
    # Normalise curved/smart double quotes to standard double quotes
    content = content.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    
    # Split by paragraph
    paragraphs = content.split("\n\n")
    
    # Active conversation tracking state machine
    last_speaker = "Unknown Character"
    active_dialogue_participants = []
    
    for p_idx, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Parse dialogue segments in quotes
        quotes = re.findall(r'"(.*?)"', paragraph)
        
        if not quotes:
            # Entire paragraph is narration
            script_rows.append({
                "Chapter": f"Chapter {idx}",
                "Character": "Narrator",
                "Text": paragraph
            })
        else:
            # Paragraph contains dialogue. Find speaker:
            detected_speaker = None
            paragraph_lower = paragraph.lower()
            
            # 1. Explicit Alias Check (First Name / Full Name)
            matched_candidates = []
            for char_name, meta in char_metadata.items():
                for alias in meta["aliases"]:
                    # Match only as word boundaries to prevent substring clashes (e.g., "Ma" in "Mara")
                    if re.search(r'\b' + re.escape(alias) + r'\b', paragraph_lower):
                        matched_candidates.append(char_name)
                        break
            
            if len(matched_candidates) == 1:
                detected_speaker = matched_candidates[0]
            elif len(matched_candidates) > 1:
                # Proximity search: find which alias is closest to the dialogue end/speaking beats
                # Default to first candidate
                detected_speaker = matched_candidates[0]
            
            # 2. Pronoun Coreference Resolver (if no explicit name is mentioned)
            if not detected_speaker:
                has_she = re.search(r'\b(she|her)\b', paragraph_lower)
                has_he = re.search(r'\b(he|him|his)\b', paragraph_lower)
                
                female_chars = [c for c, m in char_metadata.items() if m["gender"] == "female"]
                male_chars = [c for c, m in char_metadata.items() if m["gender"] == "male"]
                
                if has_she and not has_he and len(female_chars) == 1:
                    detected_speaker = female_chars[0]
                elif has_he and not has_she and len(male_chars) == 1:
                    detected_speaker = male_chars[0]
            
            # 3. Conversational Alternation Heuristic (Proximity check)
            if not detected_speaker:
                # If we are in an active conversation (alternating turns), default to the OTHER participant
                if len(active_dialogue_participants) == 2:
                    first, second = active_dialogue_participants
                    detected_speaker = second if last_speaker == first else first
                elif last_speaker != "Unknown Character" and last_speaker != "Narrator":
                    detected_speaker = last_speaker
                else:
                    detected_speaker = "Unknown Character"
                    
            # Update conversational state
            if detected_speaker and detected_speaker != "Unknown Character":
                last_speaker = detected_speaker
                if detected_speaker not in active_dialogue_participants:
                    active_dialogue_participants.append(detected_speaker)
                    if len(active_dialogue_participants) > 2:
                        active_dialogue_participants.pop(0) # Keep only last 2 active speakers
            
            # Split the paragraph into quotes and narration blocks
            marked_para = paragraph
            for q in quotes:
                marked_para = marked_para.replace(f'"{q}"', "||QUOTE_MARKER||")
                
            parts = marked_para.split("||QUOTE_MARKER||")
            
            quote_idx = 0
            for part in parts:
                part = part.strip()
                if part:
                    # Clean up connectors like "he said," or ", she replied."
                    cleaned_narration = re.sub(r'^[,\.\s\-\—]+', '', part)
                    cleaned_narration = re.sub(r'[,\.\s\-\—]+$', '', cleaned_narration)
                    if cleaned_narration and cleaned_narration not in ["she said", "he said", "said she", "said he", "replied she", "replied he"]:
                        script_rows.append({
                            "Chapter": f"Chapter {idx}",
                            "Character": "Narrator",
                            "Text": cleaned_narration
                        })
                
                if quote_idx < len(quotes):
                    script_rows.append({
                        "Chapter": f"Chapter {idx}",
                        "Character": detected_speaker,
                        "Text": quotes[quote_idx]
                    })
                    quote_idx += 1
                    
    return script_rows

def build_audiobook_script():
    draft_dir = "02_Drafting"
    output_file = "04_Publishing/audiobook_script.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    chapter_files = sorted(glob.glob(os.path.join(draft_dir, "chapter_*.md")))
    if not chapter_files:
        print("⚠️ No chapters found in 02_Drafting/.")
        return
        
    char_metadata = get_character_metadata()
    if not char_metadata:
        # Fallback metadata if story bible characters are missing
        char_metadata = {
            "Protagonist": {"gender": "male", "aliases": ["protagonist"]},
            "Antagonist": {"gender": "female", "aliases": ["antagonist"]},
            "Mentor": {"gender": "male", "aliases": ["mentor"]},
            "Sidekick": {"gender": "female", "aliases": ["sidekick"]}
        }
        
    print(f"👥 Loaded {len(char_metadata)} characters for script mapping coreference engine.")
    for char, meta in char_metadata.items():
        print(f"  • {char:<18} (Gender: {meta['gender']}, Aliases: {meta['aliases']})")
        
    all_rows = []
    for idx, filename in enumerate(chapter_files, start=1):
        chapter_rows = parse_dialogue_from_chapter(filename, idx, char_metadata)
        all_rows.extend(chapter_rows)
        
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Chapter", "Character", "Text"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)
            
    print(f"🎉 Successfully compiled audiobook script map with coreference tagging at {output_file}")

if __name__ == "__main__":
    build_audiobook_script()
