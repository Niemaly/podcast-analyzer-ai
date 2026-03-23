from flask import Flask, render_template, request, jsonify
from ai_analyzer import analyze_transcript
from ai_config import AIProfile, ToneLevel, CreativityLevel # NOWY IMPORT
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    raw_text = request.form.get('transcript')
    tone_val = request.form.get('tone', 'srednia')
    creativity_val = request.form.get('creativity', 'srednia')

    # 1. TARCZA NA PUSTY TEKST
    if not raw_text or len(raw_text.strip()) == 0:
        return jsonify({'error': 'Proszę wprowadzić tekst transkrypcji.'}), 400

    # 2. TARCZA NA ZBYT DŁUGI TEKST (Gilotyna backendowa)
    MAX_CHARS = 15000
    if len(raw_text) > MAX_CHARS:
        return jsonify({'error': f'Tekst jest za długi. Przesłano {len(raw_text)} znaków, a limit wynosi {MAX_CHARS}.'}), 400

    try:
        profil = AIProfile(
            tone=ToneLevel(tone_val),
            creativity=CreativityLevel(creativity_val)
        )
        # ... (reszta funkcji analyze, czyli wywołanie analyze_transcript i obsługa wyjątków, zostaje bez zmian) ...

        result_str = analyze_transcript(raw_text, profile=profil)
        result_json = json.loads(result_str)

        return jsonify(result_json)


    except ValueError as e:
        return jsonify({'error': f'Błędne parametry profilu: {str(e)}'}), 400
    except json.JSONDecodeError:
        return jsonify({'error': 'Model zwrócił nieprawidłowy format danych.'}), 500
    except Exception as e:
        # NOWOŚĆ: Drukujemy pełny, krwisty błąd do terminala!
        import traceback
        print("\n" + "="*40)
        print("🚨 WYKRYTO BŁĄD SERWERA 🚨")
        traceback.print_exc()
        print("="*40 + "\n")
        return jsonify({'error': f'Wystąpił błąd serwera: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)