from typing import Optional, List
from random import randint
from enum import Enum

class IntentName(str, Enum):
    YES = "yes"
    PICTO = "picto"
    HELLO = "hello"

class Entity:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

class Intent:
    def __init__(self, name: IntentName):
        self.name = name

    def __str__(self):
        return self.name


class Text:
    def __init__(self, intent: Optional[Intent], entities: List[Entity]):
        self.intent = intent
        self.entities = entities
    
    def __str__(self):
        return f"intent : {self.intent}, entities: {self.entities}"

class PictoNlp:
    def __init__(self):
        with open("words.txt", "r") as file:
            self.words = [line.rstrip() for line in file.readlines()]

    def parse(self, input: str) -> Text:
        if "oui" in input or "bien sûr" in input or "pourquoi pas" in input or "yes" in input:
            return Text(Intent(IntentName.YES), list())
        if "picto" in input or "mot" in input or "dessin" in input:
            return Text(Intent(IntentName.PICTO), list())
        if "bonjour" in input or "hey" in input or "salut" in input:
            return Text(Intent(IntentName.HELLO), list())
        return Text(None, list())

    def intentToResponse(self, intent: Intent) -> str:
        if intent.name == IntentName.PICTO or intent.name == IntentName.YES:
            random = randint(0, len(self.words)-1)
            return f"*{self.words[random]}* - 20 secondes - ✏ c'est parti !"
        if intent.name == IntentName.HELLO:
            return "Salut ! Tu veux avoir un nouveau mot à dessiner ?"
        return self.notUnderstand()

    def notUnderstand(self) -> str:
        return "Je n'ai pas compris, mais j'en apprends tous les jours.\nVoulez-vous un mot au hasard à dessiner ?"