import os
import sys
import subprocess
import time
import re
import json
from google import genai
from google.genai import types
from google.genai.errors import APIError
from dotenv import load_dotenv

# Default model definitions
DEFAULT_CREATIVE_MODEL = "gemini-2.5-flash"  # Flash model for outlining/drafting/scoring
DEFAULT_CRITIC_MODEL = "gemini-2.5-flash"    # Flash model for speed scoring (can be mapped to Pro in .env)

def load_environment():
    # Load dotenv from workspace root
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        # Check parent folder or desktop as a fallback
        load_dotenv(os.path.join(os.getcwd(), ".env"))
        api_key = os.getenv("GEMINI_API_KEY")
    return api_key

def get_gemini_client():
    api_key = load_environment()
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        print("❌ Error: GEMINI_API_KEY is not configured in '.env'.")
        sys.exit(1)
    return genai.Client(api_key=api_key)

def read_file_content(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"⚠️ Warning: Failed to read file {path}: {e}")
            return ""
    return ""

def write_file_content(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error: Failed to write to file {path}: {e}")
        return False

def run_git_command(args, cwd=None):
    try:
        result = subprocess.run(
            args,
            cwd=cwd or os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"⚠️ Git error during command '{' '.join(args)}': {e}")
        return None

def get_system_instruction(persona_filename):
    path = os.path.join(".agent", persona_filename)
    content = read_file_content(path)
    if not content:
        return f"You are a helpful creative writing assistant acting as {persona_filename}."
    return content

def get_model_config(role="creative"):
    """
    Reads 00_Story_Bible/project_manifest.json to resolve configured model overrides.
    Falls back to environment variables and defaults.
    """
    manifest_path = "00_Story_Bible/project_manifest.json"
    content = read_file_content(manifest_path)
    
    # Resolve from env first
    env_var = "CREATIVE_MODEL" if role == "creative" else "CRITIC_MODEL"
    model_override = os.getenv(env_var)
    if model_override:
        return model_override
        
    if content:
        try:
            data = json.loads(content)
            config = data.get("model_configuration", {})
            model_name = config.get(f"{role}_model")
            if model_name:
                return model_name
        except Exception:
            pass
            
    return DEFAULT_CREATIVE_MODEL if role == "creative" else DEFAULT_CRITIC_MODEL

def call_gemini(client, prompt, system_instruction, model=None, temperature=0.7, mime_type=None, max_retries=5, initial_delay=2.0):
    """
    Executes a Gemini API call with built-in exponential backoff to handle 429 rate limit errors.
    """
    delay = initial_delay
    model_name = model if model else get_model_config("creative")
    
    for attempt in range(1, max_retries + 1):
        try:
            config_args = {
                "system_instruction": system_instruction,
                "temperature": temperature
            }
            if mime_type:
                config_args["response_mime_type"] = mime_type
                
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(**config_args)
            )
            return response.text
        except APIError as e:
            if e.code == 429:
                retry_after = delay
                match = re.search(r'retry in ([\d\.]+)s', str(e), re.IGNORECASE)
                if match:
                    retry_after = float(match.group(1)) + 1.0
                print(f"  ⚠️ Gemini API rate-limited (429). Attempt {attempt}/{max_retries}. Retrying in {retry_after:.2f}s...")
                time.sleep(retry_after)
                delay = min(delay * 2.0, 16.0)
            else:
                print(f"  ❌ Gemini API Error {e.code}: {e}")
                break
        except Exception as e:
            print(f"  ❌ Error during Gemini API execution: {e}")
            break
            
    return ""
