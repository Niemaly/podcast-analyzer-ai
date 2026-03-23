import pytest
import json
from ai_social import generate_linkedin_posts

def test_generate_linkedin_posts_with_mock(mocker):
    # 1. Tworzymy atrapę odpowiedzi od Google
    falszywy_json = '''
    {
        "post_ekspercki": "To jest mądry post.",
        "post_storytelling": "Wszystko zaczęło się wczoraj...",
        "post_zaczepny": "Czy AI zabierze nam pracę?"
    }
    '''
    mock_response = mocker.MagicMock()
    mock_response.text = falszywy_json

    # 2. Podpinamy atrapę (patch) do pliku ai_social
    mocker.patch(
        'ai_social.client.models.generate_content',
        return_value=mock_response
    )

    # 3. Tworzymy sztuczne dane z podcastu
    dane_wejsciowe = {
        "tytul": "Testowy podcast",
        "podsumowanie": "Odcinek o niczym."
    }

    # 4. Odpalamy funkcję
    wynik_str = generate_linkedin_posts(dane_wejsciowe)
    wynik_json = json.loads(wynik_str)

    # 5. Sprawdzamy, czy struktura zgadza się ze schematem Pydantic
    assert "post_ekspercki" in wynik_json
    assert "post_storytelling" in wynik_json
    assert wynik_json["post_zaczepny"] == "Czy AI zabierze nam pracę?"