import pytest
import json
from ai_analyzer import analyze_transcript

def test_llm_returns_malformed_json(mocker):
    # Symulujemy sytuację, w której model zignorował schemat i zwrócił uszkodzony string
    mock_response = mocker.MagicMock()
    mock_response.text = "{ to_nie_jest_poprawny_json: urwany_tekst..."

    mocker.patch('ai_analyzer.client.models.generate_content', return_value=mock_response)

    wynik = analyze_transcript("Transkrypcja")

    # Ponieważ nasza funkcja tylko zwraca string, błąd parsowania
    # wystąpi dopiero przy próbie zrobienia json.loads() w kodzie głównym.
    with pytest.raises(json.JSONDecodeError):
        json.loads(wynik)

def test_empty_input_handled_gracefully(mocker):
    # Co jeśli wrzucimy pusty tekst? Funkcja nadal powinna wysłać zapytanie,
    # a my sprawdzamy, czy potrafi zwrócić zmockowane wartości domyślne.
    falszywy_json = '{"tytul": "Brak", "uczestnicy": [], "glowne_tematy": [], "podsumowanie": "Brak danych", "dlugosc_szacowana_min": 0}'
    mock_response = mocker.MagicMock()
    mock_response.text = falszywy_json

    mocker.patch('ai_analyzer.client.models.generate_content', return_value=mock_response)

    wynik = analyze_transcript("") # PUSTY STRING
    dane = json.loads(wynik)

    assert dane["dlugosc_szacowana_min"] == 0
    assert len(dane["uczestnicy"]) == 0