import pytest
import json
from ai_analyzer import analyze_transcript
from ai_config import AIProfile, ToneLevel, CreativityLevel

# Oznaczamy ten test, żeby nie odpalał się przypadkiem, bo zużywa darmowy limit API
@pytest.mark.real_api
def test_real_gemini_with_chill_profile():
    # Profil testowy
    profil = AIProfile(tone=ToneLevel.CALKIEM_NA_LUZIE, creativity=CreativityLevel.WYSOKA)
    tekst_testowy = "Rozmawialiśmy dziś o tym, jak działają sieci neuronowe i dlaczego matematyka jest w nich ważna. Trwało to 5 minut."

    print("\n[REAL API] Łączę się z Google Gemini. Czekaj...")

    # Odpalamy na żywym organizmie
    wynik_str = analyze_transcript(tekst_testowy, profile=profil)

    # Skoro zażądaliśmy JSONa, to musi dać się to sparsować
    wynik_json = json.loads(wynik_str)

    # Sprawdzamy podstawowe struktury
    assert "tytul" in wynik_json
    assert "podsumowanie" in wynik_json

    print("\nOto 'wyluzowane' podsumowanie prosto z API:")
    print(wynik_json["podsumowanie"])