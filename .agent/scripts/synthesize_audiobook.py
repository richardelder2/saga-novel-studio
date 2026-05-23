import os
import sys
import csv
import json
import wave
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Prebuilt voices for gemini-3.1-flash-tts-preview
VOICES = {
    "narrator": "Charon",     # Warm, expressive narrator
    "male_lead": "Fenrir",    # Rich, deep male voice
    "female_lead": "Aoede",   # Clear, expressive female voice
    "supporting_m": "Puck",   # Lighter male voice
    "supporting_f": "Kore",   # Lighter female voice
    "neutral": "Aoede"
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
            
    # 2. Heuristics based on name endings
    if char_name_lower.endswith(("a", "ia", "y", "ie", "elle", "na")):
        return VOICES["female_lead"]
        
    # Standard voice balancing
    m_count = sum(1 for v in assigned_voices.values() if v == VOICES["male_lead"])
    f_count = sum(1 for v in assigned_voices.values() if v == VOICES["female_lead"])
    
    # Default to alternating lead voices if no cues found
    return VOICES["female_lead"] if f_count <= m_count else VOICES["male_lead"]

def chunk_text(text, max_chars=4000):
    if len(text) <= max_chars:
        return [text]
        
    chunks = []
    current_chunk = ""
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

def synthesize_text_gemini(client, text, voice_name):
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-tts-preview",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["audio"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                )
            )
        )
        # Extract raw L16 PCM binary data
        part = response.candidates[0].content.parts[0]
        if part.inline_data and part.inline_data.data:
            return part.inline_data.data
        return None
    except Exception as e:
        print(f"⚠️ Error during Gemini TTS synthesis: {e}")
        return None

def save_pcm_as_wav(pcm_data, output_file, sample_rate=24000, channels=1):
    print(f"Wrapping {len(pcm_data)} raw PCM bytes in standard WAV header...")
    try:
        with wave.open(output_file, 'wb') as wav_file:
            # Set params: (nchannels, sampwidth, framerate, nframes, comptype, compname)
            # 1 channel, 16-bit (2 bytes), 24kHz sample rate
            wav_file.setparams((channels, 2, sample_rate, len(pcm_data), 'NONE', 'not compressed'))
            wav_file.writeframes(pcm_data)
        return True
    except Exception as e:
        print(f"⚠️ Error saving WAV file: {e}")
        return False

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Synthesize novel script to multi-voice WAV using Gemini native TTS.")
    parser.add_argument("--test", action="store_true", help="Generate a quick 3-sentence multi-voice audio to verify setup.")
    args = parser.parse_args()
    
    print("🎙️ COAUTHOR NATIVE GEMINI AUDIOBOOK SYNTHESIZER 🎙️")
    print("-----------------------------------------------")
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        print("❌ Error: GEMINI_API_KEY is not configured in your .env file.")
        print("Please add your key to '.env' in the root workspace folder.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    script_path = "04_Publishing/audiobook_script.csv"
    output_path = "04_Publishing/audiobook.wav"
    
    # 1. Test Mode
    if args.test:
        print("Running native Gemini multi-voice test synthesis...")
        test_rows = [
            {"Character": "Narrator", "Text": "Jax Steele adjusted his leather coat as rain beaded on his metal shoulder."},
            {"Character": "Jax Steele", "Text": "I don't care how much neon is lighting up this city, it still feels dark."},
            {"Character": "Narrator", "Text": "A voice echoed from the shadows, mechanical and smooth."}
        ]
        
        assigned_voices = {"Narrator": VOICES["narrator"], "Jax Steele": VOICES["male_lead"]}
        pcm_chunks = []
        
        for idx, row in enumerate(test_rows):
            speaker = row["Character"]
            text = row["Text"]
            voice = assigned_voices[speaker]
            print(f"-> Synthesizing test block {idx+1}: {speaker} using {voice}...")
            audio_bytes = synthesize_text_gemini(client, text, voice)
            if audio_bytes:
                pcm_chunks.append(audio_bytes)
                
        if len(pcm_chunks) == len(test_rows):
            os.makedirs("04_Publishing", exist_ok=True)
            combined_pcm = b"".join(pcm_chunks)
            if save_pcm_as_wav(combined_pcm, output_path):
                print(f"🎉 SUCCESS! Diagnostic multi-voice WAV written to: {output_path}")
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
        
    # 4. Group consecutive blocks by the same speaker
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
    pcm_chunks = []
    failed_blocks = 0
    
    for idx, row in enumerate(optimized_rows, start=1):
        speaker = row["Character"]
        text = row["Text"]
        voice = assigned_voices.get(speaker, VOICES["neutral"])
        
        # Chunk long blocks
        text_chunks = chunk_text(text)
        
        print(f"[{idx}/{len(optimized_rows)}] Synthesizing {speaker} ({len(text_chunks)} chunk(s))...")
        
        for c_idx, chunk in enumerate(text_chunks):
            audio_bytes = synthesize_text_gemini(client, chunk, voice)
            if audio_bytes:
                pcm_chunks.append(audio_bytes)
            else:
                print(f"  ⚠️ Warning: Failed to synthesize chunk {c_idx+1} for speaker '{speaker}'.")
                failed_blocks += 1
                
    # 6. Assemble WAV
    if pcm_chunks:
        combined_pcm = b"".join(pcm_chunks)
        if save_pcm_as_wav(combined_pcm, output_path):
            print("\n------------------------------------------------")
            print(f"🎉 SUCCESS! Entire multi-voice audiobook synthesized successfully!")
            print(f"Output File: {output_path}")
        else:
            print("❌ Failure during WAV creation.")
    else:
        print("\n❌ Error: No audio segments were successfully synthesized.")

if __name__ == "__main__":
    main()
