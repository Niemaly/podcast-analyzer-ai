import os
import base64
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Nie znaleziono klucza API!")

client = genai.Client(api_key=api_key)

def generate_podcast_thumbnail(podcast_data: dict) -> str:
    """
    Generuje obrazek promujący podcast i zwraca go jako string Base64.
    """
    # Wyciągamy dane z JSONa
    tematy = ", ".join(podcast_data.get("glowne_tematy", []))
    tytul = podcast_data.get("tytul", "Podcast")

    # Tworzymy prompt graficzny (modele graficzne często mają problem z pisaniem tekstu,
    # więc prosimy o obraz bez liter)
    prompt = (
        f"A professional, cinematic, eye-catching thumbnail for a LinkedIn post about a podcast. "
        f"The podcast is titled '{tytul}'. The core themes are: {tematy}. "
        "Modern corporate style, abstract tech elements, clean and minimalistic background, highly detailed. "
        "No text, no words, no letters in the image."
    )

    # Uderzamy do API generowania obrazów
    result = client.models.generate_images(
        model='imagen-3.0-generate-001', # Model z rodziny obsługującej grafiki
        prompt=prompt,
        config=dict(
            number_of_images=1,
            aspect_ratio="16:9", # Idealne proporcje na LinkedIn!
            output_mime_type="image/jpeg"
        )
    )

    # Przerabiamy surowe bajty obrazka na format Base64 (zrozumiały dla przeglądarek)
    for generated_image in result.generated_images:
        image_bytes = generated_image.image.image_bytes
        return base64.b64encode(image_bytes).decode('utf-8')

    raise ValueError("Model nie zwrócił żadnego obrazu.")