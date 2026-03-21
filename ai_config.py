from enum import Enum
from pydantic import BaseModel

class ToneLevel(str, Enum):
    SRODZE_TECHNICZNA = "srodze_techniczna"
    TECHNICZNA = "techniczna"
    SREDNIA = "srednia"
    LUZNA = "luzna"
    CALKIEM_NA_LUZIE = "calkiem_na_luzie"

class CreativityLevel(str, Enum):
    NISKA = "niska"       # Tylko fakty
    SREDNIA = "srednia"   # Balans
    WYSOKA = "wysoka"     # Duży luz i kreatywność

class AIProfile(BaseModel):
    tone: ToneLevel = ToneLevel.SREDNIA
    creativity: CreativityLevel = CreativityLevel.SREDNIA

    # TEJ FUNKCJI BRAKOWAŁO (Zwraca temperaturę dla modelu)
    @property
    def get_temperature_value(self) -> float:
        mapping = {
            CreativityLevel.NISKA: 0.2,
            CreativityLevel.SREDNIA: 0.7,
            CreativityLevel.WYSOKA: 1.3
        }
        return mapping[self.creativity]

    # TA FUNKCJA ZWRACA TWARDĄ INSTRUKCJĘ DLA MODELU
    @property
    def get_system_instruction(self) -> str:
        baza = "Jesteś API, które analizuje transkrypcje i ZAWSZE zwraca poprawny JSON. "

        instructions = {
            ToneLevel.SRODZE_TECHNICZNA: (
                "W polu 'podsumowanie' bądź surowym inżynierem i analitykiem. Używaj "
                "specjalistycznego żargonu, skup się na suchych danych i architekturze. Zero emocji."
            ),
            ToneLevel.TECHNICZNA: (
                "W polu 'podsumowanie' bądź profesjonalistą. Analizuj tekst w sposób merytoryczny "
                "i rzeczowy, zachowując techniczną terminologię."
            ),
            ToneLevel.SREDNIA: (
                "W polu 'podsumowanie' bądź obiektywnym asystentem. Twórz jasne, przystępne teksty "
                "zrozumiałe dla przeciętnego użytkownika. Unikaj skomplikowanego żargonu."
            ),
            ToneLevel.LUZNA: (
                "W polu 'podsumowanie' bądź fajnym kumplem. Pisz bezpośrednio do odbiorcy, "
                "używaj swobodnego, naturalnego języka. Skracaj dystans."
            ),
            ToneLevel.CALKIEM_NA_LUZIE: (
                "W polu 'podsumowanie' bądź totalnie wyluzowany! Rzucaj żartami, używaj nowoczesnego slangu. "
                "Tekst podsumowania ma być zabawny i napisany całkowicie na luzie."
            )
        }
        return baza + instructions[self.tone]