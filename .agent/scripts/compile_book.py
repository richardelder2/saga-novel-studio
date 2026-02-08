import os
import glob

def compile_chapters():
    draft_dir = "02_Drafting"
    output_file = "03_Review/Full_Manuscript.md"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Find all chapter files (assuming they start with 'chapter_')
    chapter_files = sorted(glob.glob(os.path.join(draft_dir, "chapter_*.md")))
    
    if not chapter_files:
        print("No chapters found in 02_Drafting/.")
        return

    with open(output_file, "w", encoding="utf-8") as outfile:
        # Add Title Page Placeholder
        outfile.write("# [Book Title]\n\n")
        outfile.write("By [Author Name]\n\n")
        outfile.write("***\n\n")
        
        for filename in chapter_files:
            with open(filename, "r", encoding="utf-8") as infile:
                content = infile.read()
                # Ensure chapter starts on a new page (standard markdown page break)
                outfile.write(content + "\n\n<div style='page-break-after: always;'></div>\n\n")
    
    print(f"Successfully compiled {len(chapter_files)} chapters into {output_file}")

if __name__ == "__main__":
    compile_chapters()
