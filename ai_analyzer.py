import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv
from ai_config import AIProfile
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Nie znaleziono klucza API!")

client = genai.Client(api_key=api_key)

# 1. Definiujemy twardy schemat, którego model NIE MOŻE złamać
class PodcastSchema(BaseModel):
    tytul: str
    uczestnicy: list[str]
    glowne_tematy: list[str]
    podsumowanie: str
    dlugosc_szacowana_min: int

# 2. Nasza główna funkcja z przywróconą nazwą i ochroną
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception)
)
def analyze_transcript(transcript_text: str, profile: AIProfile = None) -> str:
    if profile is None:
        profile = AIProfile()

    # 3. Dodajemy response_schema do konfiguracji!
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=PodcastSchema,
        temperature=profile.get_temperature_value,
        system_instruction=profile.get_system_instruction
    )

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=transcript_text,
        config=config
    )

    return response.text