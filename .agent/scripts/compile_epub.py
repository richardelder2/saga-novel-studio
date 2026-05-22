import os
import glob
import shutil

def create_epub_structure():
    epub_dir = "04_Publishing/epub_draft"
    oebps_dir = os.path.join(epub_dir, "OEBPS")
    meta_dir = os.path.join(epub_dir, "META-INF")
    
    os.makedirs(oebps_dir, exist_ok=True)
    os.makedirs(meta_dir, exist_ok=True)
    
    # 1. mimetype file
    with open(os.path.join(epub_dir, "mimetype"), "w") as f:
        f.write("application/epub+zip")
        
    # 2. META-INF/container.xml
    container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
    with open(os.path.join(meta_dir, "container.xml"), "w") as f:
        f.write(container_xml)
        
    # 3. Chapters
    draft_dir = "02_Drafting"
    chapter_files = sorted(glob.glob(os.path.join(draft_dir, "chapter_*.md")))
    
    manifest_items = []
    spine_items = []
    toc_nav_points = []
    
    for idx, filename in enumerate(chapter_files, start=1):
        ch_name = f"chapter_{idx:02d}"
        xhtml_name = f"{ch_name}.xhtml"
        xhtml_path = os.path.join(oebps_dir, xhtml_name)
        
        with open(filename, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
            
        title = f"Chapter {idx}"
        body_content = []
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                title = line[2:]
                body_content.append(f"<h1>{title}</h1>")
            elif line:
                body_content.append(f"<p>{line}</p>")
                
        xhtml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <title>{title}</title>
  <style type="text/css">
    body {{ font-family: serif; line-height: 1.5; padding: 5%; text-align: justify; }}
    h1 {{ text-align: center; font-family: sans-serif; }}
    p {{ text-indent: 1.5em; margin: 0 0 0.5em 0; }}
  </style>
</head>
<body>
  {"\n  ".join(body_content)}
</body>
</html>"""
        
        with open(xhtml_path, "w", encoding="utf-8") as f:
            f.write(xhtml_content)
            
        manifest_items.append(f'<item id="{ch_name}" href="{xhtml_name}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="{ch_name}"/>')
        toc_nav_points.append(f"""    <navPoint id="{ch_name}" playOrder="{idx}">
      <navLabel><text>{title}</text></navLabel>
      <content src="{xhtml_name}"/>
    </navPoint>""")
        
    # 4. OEBPS/toc.ncx
    toc_ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:12345"/>
    <meta name="dtb:depth" content="1"/>
  </head>
  <docTitle><text>CAMP Compiled Manuscript</text></docTitle>
  <navMap>
{"\n".join(toc_nav_points)}
  </navMap>
</ncx>"""
    with open(os.path.join(oebps_dir, "toc.ncx"), "w", encoding="utf-8") as f:
        f.write(toc_ncx)
        
    # 5. OEBPS/content.opf
    content_opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookID" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>Manuscript Export</dc:title>
    <dc:language>en</dc:language>
    <dc:identifier id="BookID">urn:uuid:12345</dc:identifier>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
{"\n".join(["    " + item for item in manifest_items])}
  </manifest>
  <spine toc="ncx">
{"\n".join(["    " + item for item in spine_items])}
  </spine>
</package>"""
    
    with open(os.path.join(oebps_dir, "content.opf"), "w", encoding="utf-8") as f:
        f.write(content_opf)
        
    # 6. Package into .epub zip file
    import zipfile
    
    epub_file_path = "04_Publishing/manuscript.epub"
    if os.path.exists(epub_file_path):
        try:
            os.remove(epub_file_path)
        except Exception:
            pass
            
    print(f"Packaging ePUB folder structure into {epub_file_path}...")
    try:
        with zipfile.ZipFile(epub_file_path, "w") as epub_zip:
            # First file must be mimetype and MUST NOT be compressed (ZIP_STORED)
            mimetype_path = os.path.join(epub_dir, "mimetype")
            epub_zip.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
            
            # Now add all other files compressed
            for root, dirs, files in os.walk(epub_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, epub_dir)
                    
                    if rel_path == "mimetype":
                        continue  # Already added
                        
                    epub_zip.write(full_path, rel_path, compress_type=zipfile.ZIP_DEFLATED)
                    
        print(f"Successfully packaged ePUB file at {epub_file_path}!")
        # Clean up draft directory to keep workspace pristine
        shutil.rmtree(epub_dir)
        print("Cleaned up temporary ePUB draft folder.")
    except Exception as e:
        print(f"Error packaging ePUB archive: {e}")

if __name__ == "__main__":
    create_epub_structure()
