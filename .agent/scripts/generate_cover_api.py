import os
import sys
import json
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

def load_project_metadata():
    title = "Untitled Book"
    genre = "Fiction"
    tone = "Vibrant and atmospheric"
    
    # 1. Read Manifest
    manifest_path = "00_Story_Bible/project_manifest.json"
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                title = data.get("title", title)
                genre = data.get("genre", genre)
        except Exception:
            pass
            
    # 2. Read Style Guide for Tone
    style_path = "00_Story_Bible/style_guide.md"
    if os.path.exists(style_path):
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Simple extraction of selected checkboxes under Tone
                tone_lines = []
                in_tone = False
                for line in content.split("\n"):
                    if "tone:" in line.lower() or "**tone:**" in line.lower():
                        in_tone = True
                        continue
                    if in_tone and line.startswith("-"):
                        if "[x]" in line.lower() or "[*]" in line.lower():
                            tone_lines.append(line.replace("-", "").replace("[x]", "").replace("[*]", "").strip())
                        elif "[ ]" not in line:
                            # If no checkbox but listed
                            tone_lines.append(line.replace("-", "").strip())
                    elif in_tone and (line.startswith("#") or line.strip() == ""):
                        if tone_lines:
                            break
                if tone_lines:
                    tone = ", ".join(tone_lines)
        except Exception:
            pass
            
    return title, genre, tone

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Generate a book cover using Google Imagen 4.0.")
    parser.add_argument("--prompt", type=str, help="Override the generated prompt with a custom one.")
    parser.add_argument("--test", action="store_true", help="Generate a quick test pattern to verify credentials.")
    args = parser.parse_args()
    
    print("🎨 COAUTHOR GRAPHIC STUDIO 🎨")
    print("----------------------------")
    
    # Load Environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        print("❌ Error: GEMINI_API_KEY is not configured in your .env file.")
        print("Please open '.env' in the root directory and add your key.")
        sys.exit(1)
        
    # Get Metadata
    title, genre, tone = load_project_metadata()
    print(f"📖 Title: {title}")
    print(f"🎭 Genre: {genre}")
    print(f"🎨 Tone cues: {tone}")
    
    # 1. Define Prompt
    if args.test:
        prompt = "A high-fidelity minimalist geometric book cover with gold foil accents, modern professional typography."
    elif args.prompt:
        prompt = args.prompt
    else:
        # Generate dynamic prompt
        prompt = (
            f"Professional cinematic book cover for a novel titled '{title}' (Genre: {genre}). "
            f"The aesthetic is {tone}. Highly atmospheric, rich deep colors, stunning lighting, dramatic composition, "
            f"minimalist and award-winning graphic design style. No raw text on the cover to allow clean layout."
        )
        
    print(f"\n🚀 Dispatching prompt to Google Imagen 4.0:\n\"\"{prompt}\"\"\n")
    
    try:
        # Initialize GenAI client
        client = genai.Client(api_key=api_key)
        
        # Call Imagen 4.0 (Which is supported by your key)
        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="3:4",  # Standard book cover aspect ratio
                output_mime_type="image/png"
            )
        )
        
        output_dir = "04_Publishing/covers"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "cover_concept.png")
        
        # Save output
        if response.generated_images:
            from io import BytesIO
            try:
                from PIL import Image
                img_data = response.generated_images[0].image.image_bytes
                image = Image.open(BytesIO(img_data))
                image.save(output_path)
                print(f"🎉 SUCCESS! Stunning book cover concept saved at: {output_path}")
            except ImportError:
                # If Pillow is not installed, write raw bytes
                img_data = response.generated_images[0].image.image_bytes
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"🎉 SUCCESS! Book cover saved as raw PNG at: {output_path} (Install 'pillow' to view in editor)")
        else:
            print("❌ Error: No images were returned by the API.")
            
    except Exception as e:
        print(f"❌ Error communicating with Google Imagen API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
