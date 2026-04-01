import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Nie znaleziono klucza API!")

client = genai.Client(api_key=api_key)

class LinkedInPostsSchema(BaseModel):
    post_ekspercki: str
    post_storytelling: str
    post_zaczepny: str

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception),
    reraise=True  # <-- DODAJ TO!
)

def generate_linkedin_posts(podcast_data: dict) -> str:
    context_text = json.dumps(podcast_data, ensure_ascii=False, indent=2)

    prompt = (
        "Jesteś doświadczonym, ale bardzo autentycznym i 'ludzkim' copywriterem na LinkedIn.\n"
        "Otrzymasz poniżej dane z przeanalizowanego podcastu.\n"
        "Twoim zadaniem jest napisanie 3 różnych postów promujących ten odcinek.\n\n"
        "🔥 WYTYCZNE DO STYLU I AUTENTYCZNOŚCI (EKSTREMALNIE WAŻNE): 🔥\n"
        "1. Posty muszą mieć 'serce' i duszę. Pisz jak człowiek z pasją, używaj emocji, czasem wtrąć coś od siebie, unikaj korporacyjnej nowomowy.\n"
        "2. Używaj formatowania tekstu: stosuj **pogrubienia** dla ważnych słów, *kursywy* dla przemyśleń, odpowiednie odstępy i wizualne wypunktowania (np. używając emoji).\n"
        "3. LUDZKI PIERWIASTEK: W każdym z 3 postów MUSISZ celowo popełnić od 1 do 3 drobnych błędów. Mogą to być literówki (np. zjedzona litera w długim słowie), brak przecinka lub mały błąd ortograficzny. Post ma wyglądać tak, jakby pisał go człowiek na telefonie w drodze do pracy.\n\n"
        "Wytyczne do konkretnych wariantów:\n"
        "1. post_ekspercki: Skupiony na merytoryce, ale przekazanej z entuzjazmem. Używaj punktów.\n"
        "2. post_storytelling: Zaczyna się od małej, osobistej historii, anegdoty lub wyzwania. Płynnie przechodzi do tematu podcastu. Buduje napięcie.\n"
        "3. post_zaczepny: Krótki, kontrowersyjny lub zadający mocne pytanie otwarte. Ma wywołać burzę w komentarzach.\n\n"
        "Pamiętaj o hashtagach na końcu.\n\n"
        f"Dane podcastu do wykorzystania:\n{context_text}"
    )

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=LinkedInPostsSchema,
        temperature=0.8,
    )

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=config
    )

    return response.text