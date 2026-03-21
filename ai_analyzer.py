from google import genai
from google.genai import types
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv

# 1. Wczytanie zmiennych z pliku .env do środowiska systemu
load_dotenv()

# 2. Pobranie klucza w bezpieczny sposób
# Magiczna sztuczka: nowe SDK Google (genai) potrafi samo znaleźć klucz,
# jeśli nazwałeś zmienną GEMINI_API_KEY. Możesz to zrobić jawnie:
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Nie znaleziono klucza API! Upewnij się, że masz plik .env z GEMINI_API_KEY.")

client = genai.Client(api_key=api_key)

# 2. Definicja struktury JSON
class PodcastAnalysis(BaseModel):
    tytul: str
    uczestnicy: list[str]
    glowne_tematy: list[str]
    podsumowanie: str
    dlugosc_szacowana_min: int

def analyze_transcript(raw_text):
    # 3. Wywołanie modelu
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=PodcastAnalysis
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Przeanalizuj transkrypcję i zwróć dane JSON: {raw_text}",
        config=config
    )
    return response.text

# 4. Przykład użycia - ukryty przed importem przez testy
if __name__ == "__main__":
    raw_podcast_text = """
    W dzisiejszym odcinku 'TechRozmowy' Adam Nowak rozmawia z Anną Kowalską 
    o przyszłości AI w medycynie. Rozmowa trwała 40 minut.
    """

    try:
        print("Łączenie z Gemini...")
        result = analyze_transcript(raw_podcast_text)

        # Przekształcenie stringa na słownik i ładne wyświetlenie
        data = json.loads(result)

        print("\n--- WYNIK ANALIZY ---")
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"\nBłąd: {e}")

