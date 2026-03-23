import pytest
import json
from app import app

# Przygotowujemy "wirtualną przeglądarkę" do testów
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_analyze_transcript_success(client, mocker):
    # Podmieniamy funkcję analizującą, żeby test był natychmiastowy
    falszywy_wynik = '{"tytul": "T", "uczestnicy": [], "glowne_tematy": [], "podsumowanie": "P", "dlugosc_szacowana_min": 5}'
    mocker.patch('app.analyze_transcript', return_value=falszywy_wynik)

    # Symulujemy wysłanie formularza (POST) z danymi
    response = client.post('/api/analyze-transcript', data={
        'transcript': 'Krótka rozmowa testowa',
        'tone': 'srednia',
        'creativity': 'srednia'
    })

    # Czy serwer odpowiedział sukcesem (HTTP 200)?
    assert response.status_code == 200

    # Czy zwrócił poprawne dane?
    data = response.get_json()
    assert data['tytul'] == 'T'

def test_api_analyze_transcript_too_long(client):
    # Generujemy tekst, który ma 15 001 znaków (przekracza limit)
    dlugi_tekst = "A" * 15001

    response = client.post('/api/analyze-transcript', data={'transcript': dlugi_tekst})

    # Serwer POWINIEN odrzucić to zapytanie z kodem 400 (Bad Request)
    assert response.status_code == 400
    assert 'zbyt długi' in response.get_json()['error']

def test_api_generate_linkedin_success(client, mocker):
    falszywe_posty = '{"post_ekspercki": "E", "post_storytelling": "S", "post_zaczepny": "Z"}'
    mocker.patch('app.generate_linkedin_posts', return_value=falszywe_posty)

    # Symulujemy wysłanie JSON-a z pierwszego etapu
    response = client.post('/api/generate-linkedin', json={'tytul': 'Test podcastu'})

    assert response.status_code == 200
    assert response.get_json()['post_ekspercki'] == "E"