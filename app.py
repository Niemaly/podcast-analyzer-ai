from flask import Flask, render_template, request, jsonify
from ai_analyzer import analyze_transcript
from ai_config import AIProfile, ToneLevel, CreativityLevel
from ai_social import generate_linkedin_posts # <-- NASZ NOWY DEPARTAMENT
import json
import traceback

app = Flask(__name__)

# --- WIDOKI (FRONTEND) ---
@app.route('/')
def index():
    return render_template('index.html')

# --- API: ETAP 1 (ANALIZA TEKSTU) ---
@app.route('/api/analyze-transcript', methods=['POST'])
def api_analyze_transcript():
    raw_text = request.form.get('transcript')
    tone_val = request.form.get('tone', 'srednia')
    creativity_val = request.form.get('creativity', 'srednia')

    if not raw_text or len(raw_text.strip()) == 0:
        return jsonify({'error': 'Proszę wprowadzić tekst transkrypcji.'}), 400

    MAX_CHARS = 15000
    if len(raw_text) > MAX_CHARS:
        return jsonify({'error': 'Przesłany tekst jest zbyt długi. Skróć transkrypcję i spróbuj ponownie.'}), 400

    try:
        profil = AIProfile(tone=ToneLevel(tone_val), creativity=CreativityLevel(creativity_val))
        result_str = analyze_transcript(raw_text, profile=profil)
        result_json = json.loads(result_str)
        return jsonify(result_json)

    except Exception as e:
        print("\n🚨 BŁĄD API ANALIZY 🚨")
        traceback.print_exc()
        return jsonify({'error': f'Wystąpił błąd analizy: {str(e)}'}), 500

# --- API: ETAP 2 (GENEROWANIE LINKEDIN) ---
@app.route('/api/generate-linkedin', methods=['POST'])
def api_generate_linkedin():
    try:
        # Ten endpoint nie przyjmuje tekstu, przyjmuje gotowego JSON-a z pierwszego etapu!
        podcast_data = request.get_json()

        if not podcast_data:
            return jsonify({'error': 'Brak danych podcastu do wygenerowania postów.'}), 400

        posts_str = generate_linkedin_posts(podcast_data)
        posts_json = json.loads(posts_str)
        return jsonify(posts_json)

    except Exception as e:
        print("\n🚨 BŁĄD API LINKEDIN 🚨")
        traceback.print_exc()
        return jsonify({'error': f'Wystąpił błąd podczas pisania postów: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)