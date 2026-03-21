import pytest
from ai_analyzer import analyze_transcript

def test_api_timeout_error(mocker):
    # Używamy side_effect, aby wymusić rzucenie wyjątku podczas wywołania
    mocker.patch(
        'ai_analyzer.client.models.generate_content',
        side_effect=ConnectionError("Brak połączenia z internetem lub timeout")
    )

    # Sprawdzamy, czy nasza aplikacja przepuszcza ten błąd wyżej
    # (lub czy go obsługuje, zależnie od tego, jak napisałeś funkcję)
    with pytest.raises(ConnectionError, match="Brak połączenia"):
        analyze_transcript("Jakiś tekst")

def test_api_500_server_error(mocker):
    # Symulacja błędu po stronie serwerów Google (np. przeciążenie)
    mocker.patch(
        'ai_analyzer.client.models.generate_content',
        side_effect=Exception("500 Internal Server Error")
    )

    with pytest.raises(Exception, match="500 Internal Server Error"):
        analyze_transcript("Kolejny tekst")