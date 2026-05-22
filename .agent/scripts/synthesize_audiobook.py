import os
import sys
import csv
import json
import base64
import requests
import argparse
from dotenv import load_dotenv

# Define premium Google TTS voices
VOICES = {
    "narrator": "en-US-Studio-O",     # Ultra-premium, highly natural Studio voice
    "male_lead": "en-US-Neural2-D",   # Clean, clear Neural2 male
    "female_lead": "en-US-Neural2-F", # Expressive Neural2 female
    "supporting_m": "en-US-Neural2-A",# Secondary male
    "supporting_f": "en-US-Neural2-E",# Secondary female
    "neutral": "en-US-Neural2-C"      # Neutral fallback
}

def guess_gender_and_assign_voice(char_name, assigned_voices):
    if char_name == "Narrator":
        return VOICES["narrator"]
        
    char_name_lower = char_name.lower()
    
    # 1. Read character profile for cues
    char_file = f"00_Story_Bible/characters/{char_name.replace(' ', '_').lower()}.md"
    if os.path.exists(char_file):
        try:
            with open(char_file, "r", encoding="utf-8") as f:
                content = f.read().lower()
                if "female" in content or "woman" in content or "girl" in content or " she " in content:
                    return VOICES["female_lead"]
                if "male" in content or "man" in content or "boy" in content or " he " in content:
                    return VOICES["male_lead"]
        except Exception:
            pass
            
    # 2. Heuristics based on common name endings or standard heuristics
    if char_name_lower.endswith(("a", "ia", "y", "ie", "elle", "na")):
        return VOICES["female_lead"]
        
    # Standard voice balancing
    m_count = sum(1 for v in assigned_voices.values() if v == VOICES["male_lead"])
    f_count = sum(1 for v in assigned_voices.values() if v == VOICES["female_lead"])
    
    # Default to alternating lead voices if no cues found
    return VOICES["female_lead"] if f_count <= m_count else VOICES["male_lead"]

def chunk_text(text, max_chars=4000):
    # Splits long text blocks along sentence boundaries
    if len(text) <= max_chars:
        return [text]
        
    chunks = []
    current_chunk = ""
    # Split by common sentence endings, keeping the punctuation
    sentences = []
    temp_sentence = ""
    for char in text:
        temp_sentence += char
        if char in ['.', '!', '?']:
            sentences.append(temp_sentence)
            temp_sentence = ""
    if temp_sentence:
        sentences.append(temp_sentence)
        
    for s in sentences:
        if len(current_chunk) + len(s) <= max_chars:
            current_chunk += s
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = s
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def synthesize_text_api(text, voice_name, api_key):
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": "en-US",
            "name": voice_name
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": 1.0,
            "pitch": 0.0
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            audio_data = base64.b64decode(res_json.get("audioContent", ""))
            return audio_data
        else:
            print(f"⚠️ API Error (Code {response.status_code}): {response.text}")
            return None
    except Exception as e:
        print(f"⚠️ Network error during synthesis: {e}")
        return None

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Synthesize novel script to multi-voice MP3 using Google Cloud TTS.")
    parser.add_argument("--test", action="store_true", help="Generate a quick 3-sentence multi-voice audio to verify setup.")
    args = parser.parse_args()
    
    print("🎙️ COAUTHOR AUDIOBOOK SYNTHESIZER 🎙️")
    print("---------------------------------")
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        print("❌ Error: GEMINI_API_KEY is not configured in your .env file.")
        print("Please add your key to '.env' in the root workspace folder.")
        sys.exit(1)
        
    script_path = "04_Publishing/audiobook_script.csv"
    output_path = "04_Publishing/audiobook.mp3"
    
    # 1. Test Mode
    if args.test:
        print("Running diagnostic multi-voice test synthesis...")
        test_rows = [
            {"Character": "Narrator", "Text": "Jax Steele adjusted his leather coat as rain beaded on his metal shoulder."},
            {"Character": "Jax Steele", "Text": "I don't care how much neon is lighting up this city, it still feels dark."},
            {"Character": "Narrator", "Text": "A voice echoed from the shadows, mechanical and smooth."}
        ]
        
        assigned_voices = {"Narrator": VOICES["narrator"], "Jax Steele": VOICES["male_lead"]}
        audio_chunks = []
        
        for idx, row in enumerate(test_rows):
            speaker = row["Character"]
            text = row["Text"]
            voice = assigned_voices[speaker]
            print(f"-> Synthesizing test block {idx+1}: {speaker} using {voice}...")
            audio_bytes = synthesize_text_api(text, voice, api_key)
            if audio_bytes:
                audio_chunks.append(audio_bytes)
                
        if len(audio_chunks) == len(test_rows):
            os.makedirs("04_Publishing", exist_ok=True)
            with open(output_path, "wb") as outfile:
                for chunk in audio_chunks:
                    outfile.write(chunk)
            print(f"🎉 SUCCESS! Diagnostic multi-voice MP3 written to: {output_path}")
        else:
            print("❌ Failure: Could not synthesize all test blocks.")
        sys.exit(0)
        
    # 2. Full Audiobook Production Mode
    if not os.path.exists(script_path):
        print(f"❌ Error: audiobook script map '{script_path}' not found.")
        print("Please run '/publish-manuscript' (Format choice 3) first to extract the dialogue script.")
        sys.exit(1)
        
    print(f"Reading dialogue script map from: {script_path}...")
    script_rows = []
    with open(script_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            script_rows.append(row)
            
    if not script_rows:
        print("❌ Error: Dialogue script is empty. Make sure chapters are drafted in 02_Drafting/.")
        sys.exit(1)
        
    print(f"Successfully loaded {len(script_rows)} narration/dialogue blocks.")
    
    # 3. Detect unique characters & map voices
    unique_characters = sorted(list(set(row["Character"] for row in script_rows)))
    print("\n👥 Detected Characters:")
    assigned_voices = {}
    for char in unique_characters:
        voice = guess_gender_and_assign_voice(char, assigned_voices)
        assigned_voices[char] = voice
        print(f"  • {char:<20} -> Voice: {voice}")
        
    # 4. Group consecutive blocks by the same speaker (Narrator merge optimization)
    print("\n⚙️ Optimizing script structure (combining contiguous speaker blocks)...")
    optimized_rows = []
    current_speaker = None
    current_text_blocks = []
    
    for row in script_rows:
        speaker = row["Character"]
        text = row["Text"].strip()
        
        if speaker == current_speaker:
            current_text_blocks.append(text)
        else:
            if current_speaker:
                optimized_rows.append({
                    "Character": current_speaker,
                    "Text": "\n\n".join(current_text_blocks)
                })
            current_speaker = speaker
            current_text_blocks = [text]
            
    if current_speaker:
        optimized_rows.append({
            "Character": current_speaker,
            "Text": "\n\n".join(current_text_blocks)
        })
        
    print(f"Combined structure from {len(script_rows)} blocks down to {len(optimized_rows)} optimized blocks.")
    
    # 5. Synthesis Loop
    print(f"\n🎙️ Synthesizing audiobook to {output_path}...")
    audio_file_assembled = 0
    failed_blocks = 0
    
    with open(output_path, "wb") as outfile:
        for idx, row in enumerate(optimized_rows, start=1):
            speaker = row["Character"]
            text = row["Text"]
            voice = assigned_voices.get(speaker, VOICES["neutral"])
            
            # Chunk long blocks (prevents Google Cloud limit)
            text_chunks = chunk_text(text)
            
            print(f"[{idx}/{len(optimized_rows)}] Synthesizing {speaker} ({len(text_chunks)} chunk(s))...")
            
            for c_idx, chunk in enumerate(text_chunks):
                audio_bytes = synthesize_text_api(chunk, voice, api_key)
                if audio_bytes:
                    outfile.write(audio_bytes)
                    audio_file_assembled += 1
                else:
                    print(f"  ⚠️ Warning: Failed to synthesize chunk {c_idx+1} for speaker '{speaker}'.")
                    failed_blocks += 1
                    
    print("\n------------------------------------------------")
    if failed_blocks == 0:
        print(f"🎉 SUCCESS! Entire multi-voice audiobook synthesized successfully!")
        print(f"Output File: {output_path}")
    else:
        print(f"⚠️ Finished with {failed_blocks} errors. Audiobook audio is incomplete.")
        
if __name__ == "__main__":
    main()
