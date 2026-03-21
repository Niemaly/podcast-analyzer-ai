import pytest
from ai_analyzer import analyze_transcript
from google.genai import types

def test_correct_model_and_parameters_are_used(mocker):
    # Zwykły mock, nie musi nic sensownego zwracać, bo interesuje nas tylko WEJŚCIE
    mock_generate = mocker.patch('ai_analyzer.client.models.generate_content')

    tekst_wejsciowy = "Tajna rozmowa o UFO"
    analyze_transcript(tekst_wejsciowy)

    # Upewniamy się, że zapytanie zostało wysłane
    mock_generate.assert_called_once()

    # Pobieramy argumenty, z jakimi wywołano 'generate_content'
    args, kwargs = mock_generate.call_args

    # 1. Asersja kontraktu: Czy używamy właściwego modelu?
    assert kwargs.get('model') == 'gemini-2.5-flash', "Ktoś zmienił model w kodzie głównym!"

    # 2. Asersja kontraktu: Czy tekst użytkownika trafił do promptu?
    assert tekst_wejsciowy in kwargs.get('contents'), "Tekst nie został przekazany do promptu!"

    # 3. Asersja kontraktu: Czy konfiguracja to obiekt GenerateContentConfig?
    assert isinstance(kwargs.get('config'), types.GenerateContentConfig), "Brakujący lub błędny format konfiguracji!"