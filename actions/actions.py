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

        
class ActionFindInfoLibro(Action):

    def name(self) -> Text:
        return "action_find_info_libro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        titolo_libro = str(tracker.get_slot('nome_libro')).lower() #Nome dello slot da prendere: nome_libro
        libro = pd.read_csv('datasets/libri.csv', encoding="UTF-8", sep=";")
        
        selections = []

        # Creo una lista  con tutti i libri il cui nome contiene il nome inserito dall'utente
        for index, row in libro.iterrows():
            if titolo_libro.lower() == row['Titolo'].lower():
                selections.append([row['Titolo']])
                break
            elif titolo_libro.lower() in row['Titolo'].lower():
                selections.append([row['Titolo']])
                
        
        if len(selections) == 1:
         #for index, row in libro.iterrows():
            if row['Titolo'] == titolo_libro:
                autore = row['Autore']
                genere = row['Genere']
                #età = row['Età']
                trama = row['Descrizione']

                message = f"Il libro '{titolo_libro}' è stato scritto da {autore} e appartiene al genere '{genere}'.\n'{titolo_libro}' è {trama}"
            else:
                message = f"Mi dispiace, non sono riuscito a trovare informazioni sul libro '{titolo_libro}'. Prova a scrivere tutto in minuscolo o forse non è presente presso la nostra libreria."
            
            dispatcher.utter_message(text=message)

            return [FollowupAction("utter_another_question"), SlotSet ("nome_libro", titolo_libro)]
           
        
        elif len(selections) > 1:
            output = "Ho trovato più libri che corrispondono al titolo che stai cercando. Per favore riformula con uno dei seguenti nomi dei libri:\n"
            for selection in selections:
                output += ('- '+selection[0]+"\n")
            dispatcher.utter_message(text=output)  
            return [AllSlotsReset()]
            
        elif len(selections) == 0:
            output = "Mmm...non ho capito bene, sei sicuro/a che il nome del libro sia corretto?"
            dispatcher.utter_message(text=output) 
            return [] 


class ActionInfoPrezzo(Action):
    def name(self) -> Text:
        return "action_info_prezzo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Estrarre l'entità dal messaggio precedente
        
        titolo_libro = tracker.get_slot("nome_libro")

        libro = pd.read_csv('datasets/libri.csv', encoding="UTF-8", sep=";")
        prezzo = None
        # Fare qualcosa con l'entità
        #if nome_libro:
        #if nome_libro == row['Titolo']:
        
        for index, row in libro.iterrows():
            if titolo_libro.lower() == row['Titolo'].lower():
              prezzo = row['Prezzo']
              break   

        if prezzo: 
            message = f"Presso la nostra libreria il libro '{titolo_libro}' è disponibile al prezzo di € {prezzo}."
        else:
            message = f"Nessun prezzo trovato."

        dispatcher.utter_message(text=message)
        return [SlotSet("nome_libro", titolo_libro)]
    

class ActionInfoEtàConsigliata(Action):
    def name(self) -> Text:
        return "action_info_età_consigliata"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Estrarre l'entità dal messaggio precedente
        
        titolo_libro = tracker.get_slot("nome_libro")

        libro = pd.read_csv('datasets/libri.csv', encoding="UTF-8", sep=";")
        # Fare qualcosa con l'entità
        età = None
        for index, row in libro.iterrows():
             if titolo_libro.lower() == row['Titolo'].lower():
              età = row['Età']
              break
        
        if età:
            # Utilizzare l'entità nel messaggio di risposta
            message = f"La lettura del libro '{titolo_libro}' è consigliata per età a partire da {età}."
        else:
            message = f"Nessuna fascia d'età trovata."

        dispatcher.utter_message(text=message)
        return [SlotSet("nome_libro", titolo_libro)]


class ActionInfoReparto(Action):
    def name(self) -> Text:
        return "action_info_reparto"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Estrarre l'entità dal messaggio precedente
        
        titolo_libro = tracker.get_slot("nome_libro")

        libro = pd.read_csv('datasets/libri.csv', encoding="UTF-8", sep=";")
        reparto = None
        scaffale = None
        # Fare qualcosa con l'entità
        
        for index, row in libro.iterrows():
             if titolo_libro.lower() == row['Titolo'].lower():
              reparto = row['Reparto']
              scaffale = row['Scaffale']
              break
          
        if reparto:
            message = f"Il libro '{titolo_libro}' è collocato nella seguente posizione:\n Reparto:{reparto} Scaffale:{scaffale}.\n\n"
        else:
            message = f"Nessuna collocazione trovata."

        dispatcher.utter_message(text=message)
        return [FollowupAction("utter_more_info")]


class ActionFindAutoreLibro(Action):

    def name(self) -> Text:
        return "action_autore_libro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        autore_libro = str(tracker.get_slot('autore_libro')) #Nome dello slot da prendere
        libro = pd.read_csv('datasets/libri.csv', encoding="UTF-8", sep=";")
        
        selections = []

        # Creo una lista  con tutti i libri il cui nome contiene il nome inserito dall'utente
        for index, row in libro.iterrows():
            if autore_libro == row['Autore']:
                selections.append([row['Titolo']])
                break
            elif autore_libro.lower() in row['Autore'].lower():
                selections.append([row['Titolo']])
             
        if selections:
            output = "I libri disponibili dell'autore che stai cercando sono i seguenti:\n"
            for selection in selections:
                output += ('- '+selection[0]+"\n")
            dispatcher.utter_message(text=output)  
            return [AllSlotsReset()]
            
        elif len(selections) == 0:
            output = "Mmm...non ho capito bene, sei sicuro/a che il nome dell'autore sia corretto?"
            dispatcher.utter_message(text=output) 
            return [] 


class ActionFindEtàLibro(Action):

    def name(self) -> Text:
        return "action_età_libro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        età_libro = str(tracker.get_slot('età_libro')) #Nome dello slot da prendere
        libro = pd.read_csv('datasets/libri.csv', encoding="UTF-8", sep=";")
        
        selections = []

        # Creo una lista  con tutti i libri il cui nome contiene il nome inserito dall'utente
        for index, row in libro.iterrows():
            if età_libro == row['Età']:
                selections.append([row['Titolo']])
                break
            elif età_libro in row['Età']:
                selections.append([row['Titolo']])
             
        if selections:
            output = "I libri disponibili per l'età che stai cercando sono i seguenti:\n"
            for selection in selections:
                output += ('- '+selection[0]+"\n")
            dispatcher.utter_message(text=output)  
            return [AllSlotsReset()]
            
        elif len(selections) == 0:
            output = "Mmm...non ho capito bene, sei sicuro/a che l'età sia corretta?"
            dispatcher.utter_message(text=output) 
            return [] 


class ActionFindGenereLibro(Action):

    def name(self) -> Text:
        return "action_genere_libro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        genere_libro = str(tracker.get_slot('genere_libro')) #Nome dello slot da prendere
        libro = pd.read_csv('datasets/libri.csv', encoding="UTF-8", sep=";")
        
        selections = []

        # Creo una lista  con tutti i libri il cui nome contiene il nome inserito dall'utente
        for index, row in libro.iterrows():
            if genere_libro == row['Genere']:
                selections.append([row['Titolo']])
                #break
            elif genere_libro in row['Genere']:
                selections.append([row['Titolo']])
             
        if selections:
            output = "I libri disponibili per il genere che stai cercando sono i seguenti:\n"
            for selection in selections:
                output += ('- '+selection[0]+"\n")
            dispatcher.utter_message(text=output)  
            return [AllSlotsReset()]
            
        elif len(selections) == 0:
            output = "Mmm...non ho capito bene, sei sicuro/a che il genere sia corretto?"
            dispatcher.utter_message(text=output) 
            return [] 