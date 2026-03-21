# 🎙️ Analizator Podcastów AI

Prosta aplikacja webowa, która wykorzystuje model Google Gemini 2.5 Flash do analizowania surowych transkrypcji podcastów lub wywiadów. Apka automatycznie wyciąga tytuł, uczestników, tematy, podsumowanie oraz szacowany czas trwania i zwraca to w wygodnym formacie JSON.

## 🛠️ Technologie
* **Backend:** Python, Flask
* **AI:** Google GenAI SDK (`gemini-2.5-flash`), Pydantic
* **Frontend:** HTML, CSS, Vanilla JS (Fetch API)
* **Testy:** Pytest, pytest-mock

## 🚀 Jak uruchomić projekt?

1. **Sklonuj repozytorium:**
   ```bash
   git clone <link-do-repozytorium>
   cd analizator-podcastow
   ```

2. **Stwórz i aktywuj środowisko wirtualne:**
   ```bash
   python -m venv .venv
   
   # Linux/Mac:
   source .venv/bin/activate
   # Windows:
   # .venv\Scripts\activate
   ```

3. **Zainstaluj wymagane biblioteki:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Dodaj klucz API:**
   Utwórz plik `.env` w głównym katalogu projektu i wklej swój klucz z Google AI Studio:
   ```text
   GEMINI_API_KEY=twój_tajny_klucz_tutaj
   ```

5. **Odpal apkę:**
   ```bash
   python app.py
   ```
   Aplikacja będzie działać pod adresem: `http://127.0.0.1:5000`

## 🧪 Testy

Aplikacja posiada testy jednostkowe. Używam biblioteki `pytest-mock` do symulowania odpowiedzi z API Google, dzięki czemu testy wykonują się ułamku sekundy i nie zużywają darmowych limitów.

Aby uruchomić wszystkie testy, wpisz:
    ```bash
    pytest
    ```