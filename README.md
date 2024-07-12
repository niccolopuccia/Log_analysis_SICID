
# Progetto di ingegneria informatica 2023/24 

## Contesto
Questo progetto si inserisce nel quadro degli sforzi per migliorare l'efficienza dei processi giudiziari in Italia.

In particolare il "Disposition Time", parametro che indica il periodo medio tra l'inizio e la conclusione di un processo giudiziario posiziona l’Italia tra i primi paesi in Europa per la durata dei processi giudiziari.
I dati evidenziano come in alcuni casi, come presso la Corte di Cassazione, questo tempo possa estendersi fino a 1156 giorni, molto al di sopra della mediana europea di 172 giorni. Questa disparità sottolinea l'importanza di adottare strategie innovative al servizio di questa causa.

Il Politecnico di Milano, nell'ambito del progetto "NEXT GENERATION UPP", si propone di inserire la componente tecnologica all’interno del contesto d’azione tramite iniziative di ricerca che esplorano l'impatto di strumenti avanzati come il data mining e il deep learning sui parametri di performance giudiziari. 

Nell'ottica di fornire una stima della qualità dei dati su cui tali analisi si basano il progetto si pone i seguenti obiettivi:
1. Studiare la consistenza dei log relativi a processi giudiziari rispetto alla descrizione del processo in termini di stati e transizioni.
2. Studiare la qualità dei dati estratti in termini di consistenza, completezza e coerenza per dimostrare che le analisi che su questi si fondano siano valide.
3. Ampliare i dizionari dati arrichendo gli stessi di nuove interpretazioni .
4. Individuare eventuali problematiche derivanti da errori nel processo di acquisizione e registrazione dati.


## Prerequisiti

Prima di iniziare è necessario assicurarsi di avere installato quanto segue:
- [MySQL Server](https://dev.mysql.com/downloads/mysql/)
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)


E' possibile installare le librerie Python richieste usando pip:
```bash
pip install mysql-connector-python pandas numpy matplotlib seaborn
```

## Importazione del Database tramite MySQL Workbench

1. **Aprire MySQL Workbench**

   Avvia MySQL Workbench sul tuo computer.

2. **Connessione al Server MySQL**

   - Clicca su `+` accanto a "MySQL Connections" per creare una nuova connessione, oppure seleziona una connessione esistente.
   - Inserisci le informazioni di connessione (hostname, username, password) e clicca su `OK` per connetterti.

3. **Aprire il Wizard di Importazione**

   - Una volta connesso, vai al menu `Server` e seleziona `Data Import`.
   
4. **Selezionare il File Dump**

   - Nella sezione "Import Options", seleziona `Import from Self-Contained File`.
   - Clicca su `...` e naviga fino al file `.mysql` che contiene il dump del database.
   
5. **Configurare le Opzioni di Importazione**

   - Nella sezione "Default Schema to be Imported To", seleziona il database di destinazione. Se il database non esiste, creane uno nuovo cliccando su `New...`.
   - Assicurati che l'opzione `Dump Structure and Data` sia selezionata.
   
6. **Avviare l'Importazione**

   - Clicca su `Start Import` per avviare il processo di importazione.
   - Attendi che l'importazione sia completata. Questo potrebbe richiedere alcuni minuti a seconda della dimensione del file dump.

7. **Verificare l'Importazione**

   - Una volta completata l'importazione, vai al menu `Schemas` nella finestra principale di MySQL Workbench.
   - Espandi il database di destinazione e verifica che le tabelle e i dati siano stati importati correttamente.


## Configurare i Parametri per la Funzione `establishConnection`

Per permettere la connessione al database intallato al passo precedente è necessario configurare opportunamente i parametri che riceve la funzione `establishConnection` il cui codice è riportato sotto:

```python

def establishConnection(hostname, username, pw, db):
    connection = None
    try:
        connection = mysql.connector.connect(host=hostname, user=username, passwd=pw, database=db)
        print("-> Connection established successfully")
    except Error as err:
        print(f"Error: '{err}'")
    return connection
```
---

La funzione `establishConnection` accetta quattro parametri che l'utente deve configurare correttamente per poter connettersi al DB:

- `hostname`: Indirizzo IP o nome del server MySQL (es. "localhost" se il server è in locale).
- `username`: Nome utente per accedere al server MySQL.
- `pw`: Password associata al nome utente per l'accesso al server MySQL.
- `db`: Nome del database a cui connettersi una volta stabilita la connessione.


**hostname:**
- Se il server MySQL è in esecuzione sulla stessa macchina locale, utilizza `"localhost"`.
- Se il server è remoto, fornisci l'indirizzo IP o il nome del server.

**username:**
- Inserisci il nome utente MySQL che ha i permessi necessari per accedere al database specificato.

**pw:**
- Inserisci la password associata al nome utente MySQL specificato. Assicurati di utilizzare le corrette maiuscole/minuscole e caratteri speciali, se presenti.

**db:**
- Specifica il nome del database a cui desideri connetterti una volta stabilita la connessione. Assicurati che questo database esista sul server MySQL e che l'utente abbia i permessi necessari per accedervi.

