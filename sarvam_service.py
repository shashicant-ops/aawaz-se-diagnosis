import base64
import io
import json
import os
import re
from pathlib import Path
from sarvamai import SarvamAI

# Load .env variables into os.environ if present as fallback
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            val = val.strip().strip("'\"")
            if val and not os.getenv(key.strip()):
                os.environ[key.strip()] = val


def get_api_key() -> str:
    """Reads SARVAM_API_KEY from st.secrets first, then os.environ / .env."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "SARVAM_API_KEY" in st.secrets:
            return st.secrets["SARVAM_API_KEY"]
    except Exception:
        pass

    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        raise ValueError("SARVAM_API_KEY not found in st.secrets, environment, or .env file.")
    return api_key


def get_sarvam_client() -> SarvamAI:
    return SarvamAI(api_subscription_key=get_api_key())


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribes English audio using Sarvam Saaras v3."""
    client = get_sarvam_client()
    audio_buffer = io.BytesIO(audio_bytes)
    
    response = client.speech_to_text.transcribe(
        file=("recording.wav", audio_buffer, "audio/wav"),
        model="saaras:v3",
        language_code="en-IN",
        mode="transcribe",
    )
    return response.transcript.strip()


def diagnose_misconception(question: str, transcript: str) -> dict:
    """Diagnoses student physics reasoning using Sarvam-105B."""
    client = get_sarvam_client()
    
    prompt = f"""You are a master JEE Physics educator diagnosing conceptual misconceptions from a student's spoken explanation.

Question Given to Student:
"{question}"

Student's Spoken Explanation:
"{transcript}"

Task:
Analyze whether the student's answer is physically sound or if it exhibits a classic JEE kinematics misconception (e.g. confusing zero velocity with zero acceleration, confusing constant speed with zero acceleration, assuming heavier objects fall faster in vacuum, etc.).

You MUST respond strictly with valid JSON conforming to this structure:
{{
  "is_correct": true or false,
  "misconception_name": "Short name of misconception, or 'None' if correct",
  "explanation_of_mistake": "Clear explanation of where the student's physics reasoning fails (or confirming why it is sound)",
  "re_teaching": "A concise 2-3 sentence explanation using an intuitive real-life analogy to correct or reinforce the concept."
}}

Output ONLY the JSON object. Do not wrap in markdown or add explanations outside the JSON."""

    response = client.chat.completions(
        model="sarvam-105b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    
    content = response.choices[0].message.content.strip()
    
    # Strip markdown backticks if any
    cleaned_content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.MULTILINE)
    cleaned_content = re.sub(r"\s*```$", "", cleaned_content, flags=re.MULTILINE).strip()
    
    return json.loads(cleaned_content)


def generate_speech(text: str, speaker: str = "aditya") -> bytes:
    """Converts re-teaching text to spoken audio using Sarvam Bulbul v3."""
    client = get_sarvam_client()
    
    response = client.text_to_speech.convert(
        text=text,
        language_code="en-IN",
        model="bulbul:v3",
        speaker=speaker,
    )
    
    if not response.audios or len(response.audios) == 0:
        raise ValueError("No audio returned by Bulbul TTS.")
        
    return base64.b64decode(response.audios[0])
