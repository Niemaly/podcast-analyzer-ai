import pytest
import json
from ai_analyzer import analyze_transcript # Importujemy Twoją funkcję

# Definiujemy zestaw danych testowych (przypadki brzegowe)
@pytest.mark.parametrize("nazwa_przypadku, tekst_wejsciowy", [
    (
            "Standardowy",
            "Rozmowa Jana z Piotrem o wędkarstwie. Trwała 15 minut. Mówili o łowieniu karpi i sprzęcie."
    ),
    (
            "Bardzo krótki",
            "To jest podcast o AI." # Brakuje czasu, uczestników itp. Model musi coś wymyślić lub dać null/0
    ),
    (
            "Tekst niezwiązany (Śmieciowy)",
            "Przepis na naleśniki: mąka, jajka, mleko. Smażyć na złoty kolor." # Model musi spróbować wpasować to w schemat podcastu
    ),
    (
            "Znaki specjalne i dziwne formatowanie",
            "W!! dzisiejszym @#$ odcinku... >>> Jan Kowalski <<< rozmawia o \n\n\n niczym. 5 min."
    )
])
def test_analyze_transcript_returns_valid_json(nazwa_przypadku, tekst_wejsciowy):
    """
    Sprawdza, czy dla różnych warunków brzegowych funkcja nadal
    zwraca poprawny strukturalnie JSON zgodny z naszym modelem Pydantic.
    """
    print(f"\nUruchamiam test: {nazwa_przypadku}")

    # Wykonanie funkcji
    wynik = analyze_transcript(tekst_wejsciowy)

    # 1. Asersja: Sprawdzamy, czy wynik w ogóle jest stringiem
    assert isinstance(wynik, str), "Wynik nie jest tekstem!"

    # 2. Asersja: Sprawdzamy, czy da się to sparsować jako JSON
    try:
        dane_json = json.loads(wynik)
    except json.JSONDecodeError:
        pytest.fail(f"Model nie zwrócił poprawnego formatu JSON dla przypadku: {nazwa_przypadku}. Zwrócił: {wynik}")

    # 3. Asersja: Sprawdzamy, czy wygenerowany JSON zawiera wszystkie wymagane klucze
    wymagane_klucze = ["tytul", "uczestnicy", "glowne_tematy", "podsumowanie", "dlugosc_szacowana_min"]
    for klucz in wymagane_klucze:
        assert klucz in dane_json, f"Brakuje klucza '{klucz}' w odpowiedzi JSON!"

    # 4. Asersja: Sprawdzamy typy danych (np. czy długość jest liczbą)
    assert isinstance(dane_json["dlugosc_szacowana_min"], int), "Długość szacowana nie jest liczbą całkowitą (int)!"
    assert isinstance(dane_json["uczestnicy"], list), "Uczestnicy nie są listą!"