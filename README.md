# ProgettoRasa

RASA Workflow

1. Posizionarsi nella directory di progetto
2. Attivare l’ambiente Rasa tramite: conda activate NOME AMBIENTE
3. Ora sono disponibili i comandi RASA (rasa train, rasa shell…):
   - ctrl c -> chiudere il bot 
   - rasa train
   - rasa shell
   - rasa shell nlu: osservare output classificatore frasi in input 
   - rasa interactive 

Per le azioni, fare parallelamente:
1. Nuova finestra di terminale
2. Posizionarsi nella directory di progetto
3. Attivare l’ambiente Rasa tramite: **conda activate NOME AMBIENTE**
4. Fare il train del modello: **rasa train**
5. Attivare il server (su una nuova finestra del terminale): **rasa run actions**


**FUNZIONALITA'**
1. orario di apertura 
2. dove si trova
3. la storia
4. che servizi offre? vendita di libri, eventi/prenotazioni, bookclub
5. ricerca libri per genere/autore/titolo/fascia d'età
6. chiedere la trama/costo
7. Eventualmente prenotazione libri
