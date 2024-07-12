# Funzioni Python per l'analisi e la gestione di dati da database MySQL

Qui di seguito è fornita la documentazione per le funzioni Python implementate per l'analisi e la gestione dei dati da un database MySQL. Le funzioni sono progettate per diverse operazioni di estrazione, manipolazione e visualizzazione dei dati.

## `enstablishConnection`

Questa funzione permette di stabilire una connessione al server MySQL e restituisce l'oggetto di connessione.

### Parametri
- `hostname`: Nome host del server MySQL
- `username`: Nome utente per l'accesso al server
- `pw`: Password per l'accesso
- `db`: Nome del database a cui connettersi

### Ritorno
- Oggetto di connessione al server MySQL

---

## `extract`

Questa funzione permette di estrarre dati dal database in modalità lettura.

### Parametri
- `connection`: Oggetto di connessione al server MySQL
- `query`: Query SQL per l'estrazione dei dati
- `parameter`: Parametri da passare alla query SQL

### Ritorno
- Risultato della query eseguita

---

## `getDataframe`

Questa funzione converte il risultato di una query SQL in un DataFrame Pandas con uno schema specifico per una tabella data.

### Parametri
- `queryRes`: Risultato della query SQL
- `table`: Nome della tabella per cui si desidera ottenere lo schema

### Ritorno
- DataFrame Pandas con lo schema specifico della tabella

---

## `describeTable`

Questa funzione stampa le prime 10 righe di un DataFrame Pandas ottenuto da una query SQL e fornisce informazioni sul DataFrame.

### Parametri
- `queryRes`: Risultato della query SQL
- `table`: Nome della tabella da descrivere

---

## `plotAttributeDistr`

Questa funzione permette di tracciare la distribuzione di un attributo specifico di una tabella in un grafico a barre.

### Parametri
- `queryRes`: Risultato della query SQL
- `attr`: Attributo da analizzare
- `table`: Nome della tabella da cui estrarre i dati

---

## `loopsTransactionsGlobalCount`

Questa funzione calcola e visualizza il conteggio dei cicli (self-loops) rispetto al numero totale di transazioni in una tabella.

### Parametri
- `queryRes`: Risultato della query SQL
- `table`: Nome della tabella da cui estrarre i dati

---

## `loopsTransactionsLocalCount`

Questa funzione calcola e visualizza la percentuale di cicli (self-loops) rispetto al totale delle transizioni partendo da ciascuno stato in una tabella.

### Parametri
- `queryRes`: Risultato della query SQL
- `table`: Nome della tabella da cui estrarre i dati

### Ritorno
- Stati sink (terminale) trovati

---

## `eventsToSinkStates`

Questa funzione elenca tutti gli eventi che portano a stati sink (terminali) in modo da estrarne le descrizioni dalla tabella degli eventi.

### Parametri
- `queryStatiEventi`: Risultato della query SQL per la tabella `statievento`
- `queryEventi`: Risultato della query SQL per la tabella `eventi`
- `sink_states`: Stati terminali trovati dalla funzione `loopsTransactionsLocalCount`
- `table1`: Nome della tabella `statievento`
- `table2`: Nome della tabella `eventi`

---

## `duplicateSearch`

Questa funzione permette di trovare tutte le righe duplicate in una tabella.

### Parametri
- `queryRes`: Risultato della query SQL
- `table`: Nome della tabella da cui estrarre i dati

---

## `numprvCoverage`

Questa funzione valuta se un attributo ha un valore unico per ogni riga nella tabella o se ci sono valori mancanti o duplicati.

### Parametri
- `queryRes`: Risultato della query SQL
- `table`: Nome della tabella da cui estrarre i dati
- `attr`: Attributo da valutare

---

## `outcomeFromEventDescription`

Questa funzione analizza gli esiti degli eventi di tipo '2E' e 'O2' basandosi sulle descrizioni associate agli eventi.

### Parametri
- `queryRes`: Risultato della query SQL

---

## `riformataVsCtiposDomain`

Questa funzione stampa la distribuzione dei valori nelle colonne `RIFORMATA` e `CTIPOS` di una tabella.

### Parametri
- `queryRes`: Risultato della query SQL
- `table`: Nome della tabella da cui estrarre i dati

---

## `whenRiformataFullCtiposSameVal`

Questa funzione verifica se la dichiarazione "quando Riformata è piena, Ctipos ha lo stesso valore" è vera o meno.

### Parametri
- `queryRes`: Risultato della query SQL
- `table`: Nome della tabella da cui estrarre i dati

---

## `lettersMeaning`

Questa funzione analizza la distribuzione degli esiti degli eventi più frequenti nella tabella `stor` associati a ogni valore di `RIFORMATA` e `CTIPOS`.

---

## `lastOutcomePerProcess`

Questa funzione restituisce solo l'ultima occorrenza di un evento di esito nello stesso processo, per evitare correzioni che moltiplicano il numero di eventi.

### Parametri
- `joinedTable`: Risultato della query SQL con dati combinati

### Ritorno
- Lista delle ultime occorrenze di eventi di esito per processo

---

## `correctionEventsCounter`

Questa funzione conta gli eventi nella tabella `stor` che hanno 'correzione' nella loro descrizione e ne calcola la percentuale rispetto al totale delle righe.

### Parametri
- `correctionCount`: Numero di eventi di correzione nella tabella
- `rowCount`: Numero totale di righe nella tabella `stor`

---

## `flowDeviationDiscovery`

Questa funzione individua gli eventi di correzione nella tabella `stor` che causano deviazioni di flusso rispetto all'evento precedente.

### Parametri
- `queryRes`: Risultato della query SQL

### Ritorno
- Lista di eventi che causano deviazioni di flusso

---

## `specificEventCounter`

Questa funzione conta le occorrenze di un evento specifico nella tabella `stor` e ne calcola la percentuale rispetto al totale delle righe.

### Parametri
- `eventCount`: Numero di eventi di un tipo specifico nella tabella
- `rowCount`: Numero totale di righe nella tabella `stor`
- `event`: Evento specifico da contare

---

## `flowDeviationDiscoverySubsetted`

Questa funzione esegue un'analisi delle deviazioni di flusso escludendo gli eventi contrassegnati con 'C9' dalla tabella `stor`.

### Parametri
- `queryRes`: Risultato della query SQL

### Ritorno
- Numero di eventi di correzione sopravvissuti dopo l'esclusione di 'C9'

---

## `survivedCorrectionDescribe`

Questa funzione descrive la distribuzione degli eventi di correzione sopravvissuti, escludendo quelli associati a cambiamenti di stato o rituale.

### Parametri
- `result`: Risultato della query SQL

---

## `survivedNotRiteCorrectionDescribe`

Questa funzione descrive la distribuzione degli eventi di correzione sopravvissuti che non sono associati a cambiamenti di stato o rituale.

### Parametri
- `result`: Risultato della query SQL

---

## `printRowContainingRit`

Questa funzione stampa le righe della tabella `stor` contenenti 'rito' o 'ritualità' nella descrizione dell'evento per inferire i relativi codici `CCDOEV`.

### Parametri
- `queryRes`: Risultato della query SQL

---

## `ritualityChanges`

Questa funzione conta il numero totale di eventi che coinvolgono cambiamenti di rituale nella tabella `stor`.

### Parametri
- `queryRes`: Risultato della query SQL

---

## `showC0Changes`

Questa funzione mostra le transizioni da un rito all'altro quando si verifica un evento di correzione della ritualità.

### Parametri
- `queryRes`: Risultato della query SQL

---

## `plotIDGRPEV`

Questa funzione traccia la distribuzione di ogni valore di `IDGRPEV` in una tabella.

### Parametri
- `distinctAttr`: Attributi distinti della tabella

---

---

## `inferMeaning`

Questa funzione analizza e stampa la descrizione degli eventi più frequenti associati a IDGRPEV specifici nel dataframe `stor`.

### Parametri
- `QueryRes`: Risultato della query SQL contenente gli eventi da analizzare
- `labels`: Etichette degli IDGRPEV di interesse

---

## `verticalConsistencyCheck`

Questa funzione scrive un file di testo formattando i risultati della query in modo che siano facili da elaborare per la funzione `iterOnFile`.

### Parametri
- `queryRes`: Risultato della query SQL contenente le occorrenze degli eventi

---

## `iterOnFile`

Questa funzione legge un file di testo e rileva le inconsistenze temporali verticali.

### Parametri
- `fileName`: Nome del file da leggere

---

## `horizontalConsistencyCheck`

Questa funzione scrive un file di testo formattando i risultati della query per facilitare l'elaborazione da parte della funzione `iterOnFile2`.

### Parametri
- `queryRes`: Risultato della query SQL contenente le informazioni sull'evento

---

## `iterOnFile2`

Questa funzione legge un file di testo e rileva le inconsistenze orizzontali temporali tra le date di registrazione e modifica degli eventi.

### Parametri
- `fileName`: Nome del file da leggere

---

## `sameDayDifferentRegOrMod`

Questa funzione identifica le righe nella tabella `stor` in cui lo stesso evento ha date di registrazione o modifiche diverse nello stesso giorno.

### Parametri
- `queryRes`: Risultato della query SQL contenente le righe duplicate

---

## `areTheSameTable`

Questa funzione confronta due versioni diverse della tabella `stati eventi` per identificare le differenze.

### Parametri
- `queryRes`: Risultato della query SQL che ritorna le differenze tra le tabelle

---

## `invisibilityDiscovery`

Questa funzione verifica se ci sono eventi contrassegnati come invisibili nella tabella degli eventi di stato ma che compaiono nei log.

### Parametri
- `invisibleEvent`: Elenco degli eventi invisibili
- `history`: Log storici contenenti gli eventi

---

## `printMatrix`

Questa funzione stampa una matrice che mostra quante volte c'è una corrispondenza tra i valori di `RIFORMATA` e `CTIPOS` e quante volte si verifica una discrepanza.

### Parametri
- `queryRes`: Risultato della query SQL contenente i valori di `RIFORMATA` e `CTIPOS`

---

## `compareDescription`

Questa funzione confronta la descrizione degli eventi nella tabella `stor` con i valori di `RIFORMATA` e `CTIPOS`.

---


