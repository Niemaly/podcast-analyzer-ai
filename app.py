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

    # 1. Pobieramy nowe parametry z formularza (lub ustawiamy domyślne)
    tone_val = request.form.get('tone', 'srednia')
    creativity_val = request.form.get('creativity', 'srednia')

    if not raw_text or len(raw_text.strip()) == 0:
        return jsonify({'error': 'Proszę wprowadzić tekst transkrypcji.'}), 400

    try:
        # 2. Tworzymy obiekt Pydantic. Jeśli ktoś wyśle z HTMLa niepoprawną
        # wartość (np. "super_hiper_luz"), Pydantic od razu wyrzuci błąd (ValueError)
        profil = AIProfile(
            tone=ToneLevel(tone_val),
            creativity=CreativityLevel(creativity_val)
        )

        # 3. Przekazujemy tekst ORAZ profil do naszej funkcji AI
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