import os
import glob
import re
import csv

def parse_dialogue_from_chapter(filename, idx, char_list):
    script_rows = []
    
    with open(filename, "r", encoding="utf-8") as infile:
        content = infile.read()
        
    # Split by paragraph
    paragraphs = content.split("\n\n")
    
    for p_idx, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Parse dialogue in quotes
        quotes = re.findall(r'"(.*?)"', paragraph)
        
        if not quotes:
            # Entire paragraph is narration
            script_rows.append({
                "Chapter": f"Chapter {idx}",
                "Character": "Narrator",
                "Text": paragraph
            })
        else:
            # Paragraph contains dialogue. Let's find the speaker
            # Find words capitalized that might be character names
            detected_char = "Narrator"
            for char in char_list:
                if char.lower() in paragraph.lower():
                    # High probability this character is speaking or tagged in this paragraph
                    detected_char = char
                    break
                    
            # Split the paragraph into quotes and narration blocks
            # We replace each quote with a marker, then split
            marked_para = paragraph
            for q in quotes:
                marked_para = marked_para.replace(f'"{q}"', "||QUOTE_MARKER||")
                
            parts = marked_para.split("||QUOTE_MARKER||")
            
            quote_idx = 0
            for part in parts:
                part = part.strip()
                if part:
                    # Clean up grammar connectors like "he said," or ", she replied."
                    cleaned_narration = re.sub(r'^[,\.\s\-\—]+', '', part)
                    cleaned_narration = re.sub(r'[,\.\s\-\—]+$', '', cleaned_narration)
                    if cleaned_narration:
                        script_rows.append({
                            "Chapter": f"Chapter {idx}",
                            "Character": "Narrator",
                            "Text": cleaned_narration
                        })
                
                if quote_idx < len(quotes):
                    # We have a quote. Let's assign speaker
                    speaker = detected_char if detected_char != "Narrator" else "Unknown Character"
                    script_rows.append({
                        "Chapter": f"Chapter {idx}",
                        "Character": speaker,
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
        print("No chapters found in 02_Drafting/.")
        return
        
    # Get a list of known character names from the characters folder
    char_list = []
    char_dir = "00_Story_Bible/characters"
    if os.path.exists(char_dir):
        for char_file in os.listdir(char_dir):
            if char_file.endswith(".md"):
                char_name = os.path.splitext(char_file)[0]
                # Capitalize first letter
                char_list.append(char_name.replace("_", " ").title())
                
    # Fallback default character names if directory is empty
    if not char_list:
        char_list = ["Protagonist", "Antagonist", "Mentor", "Sidekick"]
        
    all_rows = []
    for idx, filename in enumerate(chapter_files, start=1):
        chapter_rows = parse_dialogue_from_chapter(filename, idx, char_list)
        all_rows.extend(chapter_rows)
        
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Chapter", "Character", "Text"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)
            
    print(f"Successfully compiled audiobook script map at {output_file}")

if __name__ == "__main__":
    build_audiobook_script()
