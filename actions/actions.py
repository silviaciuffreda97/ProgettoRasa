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
from rasa.shared.nlu.constants import ENTITIES

class ActionInfoLibro(Action):

    def name(self) -> Text:
        return "action_info_libro"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        titolo_libro = str(tracker.get_slot('nome_libro')).lower()  # Nome dello slot da prendere: nome_libro

        if isinstance(titolo_libro, str):
          titolo = titolo_libro
        else:
            titolo_entity = next((entity for entity in tracker.latest.message.get('entities') if entity.get('entity') == 'nome_libro'), None) 
            if titolo_entity:
                titolo = titolo_entity.get('value')
            else:
                 titolo = None
  
        libro = pd.read_csv('datasets/libri.csv', encoding="UTF-8", sep=",")

        try:
            autore = libro[libro['Titolo'] == titolo]['Autore'].values[0]
            message = f"L'autore del libro '{titolo}' è: {autore}."
        except:
            message = f"Mi dispiace, non sono riuscito a trovare informazioni sull'autore del libro '{titolo}'."

        dispatcher.utter_message(text=message)

        return []


    