import os
import base64
from google import genai
from google.genai import types # <-- DODANY IMPORT (Wymagany do nowej konfiguracji)
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Nie znaleziono klucza API!")

client = genai.Client(api_key=api_key)

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=15),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception),
    reraise=True  # <-- DODAJ TO!
)

def generate_podcast_thumbnail(podcast_data: dict) -> str:
    """
    Generuje obrazek promujący podcast i zwraca go jako string Base64.
    """
    # Wyciągamy dane z JSONa
    tematy = ", ".join(podcast_data.get("glowne_tematy", []))
    tytul = podcast_data.get("tytul", "Podcast")

    # Tworzymy prompt graficzny
    prompt = (
        f"A professional, cinematic, eye-catching thumbnail for a LinkedIn post about a podcast. "
        f"The podcast is titled '{tytul}'. The core themes are: {tematy}. "
        "Modern corporate style, abstract tech elements, clean and minimalistic background, highly detailed. "
        "No text, no words, no letters in the image."
    )

    # Uderzamy do API generowania obrazów (ZAKTUALIZOWANA NAZWA MODELU!)
    result = client.models.generate_images(
        model='imagen-4.0-generate-001', # <-- ZMIANA TUTAJ
        prompt=prompt,
        config=types.GenerateImagesConfig( # <-- ZMIANA TUTAJ
            number_of_images=1,
            aspect_ratio="16:9",
            output_mime_type="image/jpeg"
        )
    )

    # Przerabiamy surowe bajty obrazka na format Base64
    for generated_image in result.generated_images:
        image_bytes = generated_image.image.image_bytes
        return base64.b64encode(image_bytes).decode('utf-8')

    raise ValueError("Model nie zwrócił żadnego obrazu.")