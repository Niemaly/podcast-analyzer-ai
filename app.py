from flask import Flask, render_template, request, jsonify
from ai_analyzer import analyze_transcript
import json

app = Flask(__name__)

# 1. Główny widok - ładuje nasz plik HTML
@app.route('/')
def index():
    return render_template('index.html')

# 2. Endpoint API - przyjmuje tekst, pyta Gemini i zwraca wynik
@app.route('/analyze', methods=['POST'])
def analyze():
    # Pobieramy tekst wysłany z formularza
    raw_text = request.form.get('transcript')

    if not raw_text or len(raw_text.strip()) == 0:
        return jsonify({'error': 'Proszę wprowadzić tekst transkrypcji.'}), 400

    try:
        # Wywołujemy naszą funkcję z pliku ai_analyzer.py
        result_str = analyze_transcript(raw_text)

        # Parsujemy odpowiedź z Gemini, aby upewnić się, że to czysty JSON
        result_json = json.loads(result_str)

        # Zwracamy ładny JSON do przeglądarki
        return jsonify(result_json)

    except json.JSONDecodeError:
        return jsonify({'error': 'Model zwrócił nieprawidłowy format danych.'}), 500
    except Exception as e:
        return jsonify({'error': f'Wystąpił błąd serwera: {str(e)}'}), 500

if __name__ == '__main__':
    # Uruchamiamy serwer w trybie deweloperskim
    app.run(debug=True)