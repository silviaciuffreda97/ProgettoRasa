# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



import pandas as pd
from pathlib import Path
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset


class ActionInfoLibro(Action):

    def name(self) -> Text:
        return "action_info_libro"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        titolo_libro = str(tracker.get_slot('nome_libro')).lower()  # Nome dello slot da prendere: nome_libro
  
        libro = pd.read_csv('datasets/libri.csv', encoding="UTF-8", sep=";")

        try:
            autore = libro[libro['Titolo'] == titolo_libro]['Autore'].values[0]
            genere = libro[libro['Titolo'] == titolo_libro]['Genere'].values[0]
            eta = libro[libro['Titolo'] == titolo_libro]['Età'].values[0]
           # prezzo = libro[libro['Titolo'] == titolo_libro]['Prezzo'].values[0]
            descrizione = libro[libro['Titolo'] == titolo_libro]['Descrizione'].values[0]

            message = f"Il libro '{titolo_libro}' è stato scritto da {autore} ed appartiene al genere '{genere}'.\n'{titolo_libro}' è {descrizione}"
        except:
            message = f"Mi dispiace, non sono riuscito a trovare informazioni sull'autore del libro '{titolo_libro}'."

        dispatcher.utter_message(text=message)

        return []


    