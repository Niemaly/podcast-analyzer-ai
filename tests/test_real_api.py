import pytest
import json
import os
from datetime import datetime
from ai_analyzer import analyze_transcript
from ai_config import AIProfile, ToneLevel, CreativityLevel
from ai_social import generate_linkedin_posts

# Upewniamy się, że folder na raporty istnieje
REPORTS_DIR = "test_reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def save_report(prefix_name: str, data: dict):
    """Pomocnicza funkcja do serializacji wyników do pliku JSON."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{REPORTS_DIR}/{prefix_name}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@pytest.mark.real_api
def test_real_gemini_with_chill_profile():
    profil = AIProfile(tone=ToneLevel.CALKIEM_NA_LUZIE, creativity=CreativityLevel.WYSOKA)
    tekst_testowy = "Rozmawialiśmy dziś o tym, jak działają sieci neuronowe i dlaczego matematyka jest w nich ważna. Trwało to 5 minut."

    # Pobieramy wynik z API
    wynik_str = analyze_transcript(tekst_testowy, profile=profil)
    wynik_json = json.loads(wynik_str)

    # Asersje (czy model wykonał zadanie)
    assert "tytul" in wynik_json
    assert "podsumowanie" in wynik_json

    # SERIALIZACJA: Zapisujemy odpowiedź do pliku
    save_report("analiza_api", wynik_json)

@pytest.mark.real_api
def test_real_gemini_social_posts():
    dane_wejsciowe = {
        "tytul": "Przyszłość programowania",
        "uczestnicy": ["Jan Kowalski", "Anna Nowak"],
        "glowne_tematy": ["AI", "Python", "Rynek Pracy"],
        "podsumowanie": "Rozmowa o tym, jak AI wpływa na pracę programistów. Główny wniosek: AI nie zabierze nam pracy, ale programiści używający AI zastąpią tych, którzy jej unikają."
    }

    # Odpalamy połączenie do prawdziwego API
    wynik_str = generate_linkedin_posts(dane_wejsciowe)
    wynik_json = json.loads(wynik_str)

    # Asersje schematu Pydantic
    assert "post_ekspercki" in wynik_json
    assert "post_storytelling" in wynik_json
    assert "post_zaczepny" in wynik_json

    # SERIALIZACJA: Zapisujemy wygenerowane posty do pliku
    save_report("linkedin_api", wynik_json)
