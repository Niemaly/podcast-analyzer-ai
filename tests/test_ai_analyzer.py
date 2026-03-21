import pytest
import json
from ai_analyzer import analyze_transcript

def test_analyze_transcript_with_mock(mocker):
    """
    Test weryfikujący logikę naszej aplikacji bez wysyłania
    prawdziwego zapytania do Google API (działa w ułamku sekundy).
    """
    print("\n[MOCK] Uruchamiam test z atrapą API...")

    # 1. Przygotowujemy fałszywą odpowiedź JSON, którą chcemy, aby "zwróciło" API
    falszywy_json = '''
    {
        "tytul": "Zmockowany Podcast",
        "uczestnicy": ["Jan Testowy", "Anna Atrapa"],
        "glowne_tematy": ["Mockowanie", "Testy jednostkowe"],
        "podsumowanie": "To jest test bez użycia prawdziwego API. Działa błyskawicznie!",
        "dlugosc_szacowana_min": 10
    }
    '''

    # 2. Tworzymy atrapę obiektu odpowiedzi.
    # Funkcja w ai_analyzer.py robi `return response.text`,
    # więc nasz mock musi mieć pole `.text` z naszym sztucznym JSONem.
    mock_response = mocker.MagicMock()
    mock_response.text = falszywy_json

    # 3. PATCHOWANIE (Podmiana)
    # Przechwytujemy wywołanie 'client.models.generate_content' w pliku 'ai_analyzer'
    # i każemy mu zwrócić naszą atrapę (mock_response).
    mock_generate_content = mocker.patch(
        'ai_analyzer.client.models.generate_content',
        return_value=mock_response
    )

    # 4. Wykonujemy naszą funkcję z dowolnym tekstem.
    # Zapytanie NIE poleci do sieci, zostanie przechwycone przez mocka.
    tekst_wejsciowy = "Byle jaki tekst. Bla bla bla. Model i tak tego nie przeczyta."
    wynik = analyze_transcript(tekst_wejsciowy)

    # 5. Sprawdzamy, czy nasz kod poprawnie przetworzył odpowiedź
    dane_json = json.loads(wynik)

    # 6. Asersje: sprawdzamy, czy otrzymaliśmy dokładnie to, co podłożyliśmy w mocku
    assert dane_json["tytul"] == "Zmockowany Podcast", "Tytuł się nie zgadza!"
    assert dane_json["dlugosc_szacowana_min"] == 10, "Długość się nie zgadza!"
    assert len(dane_json["uczestnicy"]) == 2, "Błędna liczba uczestników!"

    # 7. Weryfikacja: sprawdzamy, czy funkcja wysyłająca zapytanie została w ogóle wywołana przez nasz kod
    mock_generate_content.assert_called_once()

    print("[MOCK] Test zakończony sukcesem w ułamku sekundy!")