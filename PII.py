#Progetto Ingegneria Informatica

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import pandas as pd
import numpy as np
from numpy import zeros
import matplotlib.pylab as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns
plt.style.use('ggplot')
# pd.set_option('display.max_rows', None)

#FUNCTION DEFINITION AREA:

# Allows to establish mySQL server-Python connection and returns an item which grants the access to data in the server
def enstablishConnection(hostname, username, pw, db):
    connection = None
    try:
        connection = mysql.connector.connect(host = hostname, user = username, passwd = pw, database = db)
        print("-> Conection enstablished successfully")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

# Allows to extract data from the database in read mode
def extract(connection, query, parameter):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, parameter)
        result = cursor.fetchall()
        # print("-> Database queried successfully")
        return result
    except Error as err:
        print(f"Error: '{err}'")

# Allows to get the dataframe from a query with the proper schema
def getDataframe(queryRes, table):
    df = pd.DataFrame(queryRes)
    tableSchema = []
    match (table):
        case 'statievento': tableSchema = ['RITUALITA', 'CURSTATE', 'IDGRPEV', 'IDEVENTO', 'NEWSTATE', 'FKEVENTPROCS', 'IDSTATIEVENTI', 'COLLEGIALITATRIB', 'COLLEGIALITACDA', 'ISVISIBLE']
        case 'eventi':  tableSchema = ['CCDOEV', 'CDESCR', 'CDESTO', 'TIPOEVENTO', 'HIDDEN']
        case 'stor': tableSchema = ['NUMPRO', 'NUMPRV', 'CCDOEV', 'CTIPSE', 'NUMGIU', 'DATAEV', 'CCODST', 'CNPARA', 'CDESCR', 'DATARE', 'CODUTE', 'CEVPAD', 'CSTAPR', 'ISVISIBLE', 'CRONOLOGICO', 'IDTIPOATTOCRONOLOGICO', 'DATAULTIMAMODIFICA', 'PARAMS', 'NOTA', 'IDDOCS']
        case 'defi': tableSchema = ['NUMPRO', 'NUMPRV', 'CANNRV', 'CNUMRV', 'DATUDE', 'DACONC', 'DAREPL', 'DATDEC', 'DATDEP', 'DATCOP', 'DATRES', 'DATPUB', 'CTIPDE', 'CTIPOS', 'NUMGIU', 'CTIPSE', 'CORGIU', 'RIFORMATA', 'DINVCOLL', 'DRITCOLL', 'DINVREL', 'DRITREL', 'FKREPE', 'ARCHIVIOGIUR', 'PQM']
        case 'fasc': tableSchema = ['NUMPRO', 'CANRUO', 'CNURUO', 'DISCRI', 'CATTOI', 'COSTGI', 'CTIPSE', 'CANNSE', 'CNUMSE', 'NUMGIU', 'CCODST', 'CSTAPR', 'CTIPRI', 'CCODGI', 'DCOMPA', 'DPROUD', 'DORAUD', 'CEUENT', 'DEVENT', 'NIMPOR', 'NVALOR', 'NANNMA', 'CTRASC', 'DDADEF', 'CTIDEF', 'CVELIN', 'CNUMCC', 'CANNCC', 'CCODUF', 'CTIPPR', 'CSUBPR', 'LAST_UPDATE', 'ANNOGIUDICE', 'RUOLOGIUDICE', 'COLLEGIALE', 'ESENZIONECONTRUNIF', 'CODICEOGGETTO', 'IMPORTOCONTRUNIF', 'SAVEGIUDXRIUN', 'SAVESEZXRIUN', 'SAVESTATXRIUN', 'SAVESEZXFERIALE', 'SAVEGIUDXFERIALE', 'SUBTYPE', 'RIASSCASSAZIONE', 'FLAGPA', 'USER_PREISCR', 'BARCODE', 'IDREPFASC', 'DATAULTIMAMODIFICA', 'CLASS_ACT', 'IMPORTOSANZIONE', 'NOTESANZIONE', 'IDSS', 'CNTISTANZA']
    df.columns = tableSchema
    return df

#Allows to describe the structure of the table
def describeTable(queryRes, table):
    df = getDataframe(queryRes, table)
    print(df.head(10))
    print("Infos:")
    print(df.info())

#Allows to plot the distribution of some attributes in stati_evento table
def plotAttributeDistr(queryRes, attr, table):
    df = getDataframe(queryRes, table)
    attr_occurrences = df[attr].value_counts()
    attr_occurrences.plot(kind='bar', title=f'Distribution of {attr} occurrences', color='#3A9282')
    plt.xlabel(attr)
    plt.ylabel('Occurrences')
    plt.show()

#Allows to analyze the self_loops / normal transition ratio
def loopsTransactionsGlobalCount(queryRes, table):
    df = getDataframe(queryRes, table)
    self_loops = len(df[df['NEWSTATE'] == "++"])
    transactions = len(df)

    print("The total number of transactions is:", transactions)
    print("The total number of self-loops is:", self_loops)

    labels = ['loops', 'rest']
    sizes = [self_loops, transactions]

    plt.bar(labels, sizes, color = '#3A9282', width=0.4)
    plt.show()

    loops_percentage = (self_loops/transactions)*100
    rest_percentage = ((transactions-self_loops)/transactions)*100
    labels = ['loops_percentage', 'rest_percentage']
    sizes = [loops_percentage, rest_percentage]
    colors = ['#3A9282', '#DBA37E']
    plt.pie(sizes, labels= labels,autopct='%1.1f%%', startangle=90, colors = colors)
    plt.title('Loops vs normal transaction Proportions')
    plt.axis('equal')
    plt.show()

# Returns for each state how many loops are there compared with the total number of transactions starting from that state
def loopsTransactionsLocalCount(queryRes, table):
    df = getDataframe(queryRes, table)
    start_state = df["CURSTATE"].unique()
    loop_percentage = []
    sink_states = []

    for state in start_state:
        loops = len(df.query("(CURSTATE == @state) & (NEWSTATE == '++')"))
        tot = len(df.query("CURSTATE == @state"))
        percentage = (loops/tot)*100
        loop_percentage.append(percentage)
        if (percentage == 100):
            sink_states.append(state)

    comparison = {'state' : start_state, 'perc' : loop_percentage}
    new_table= pd.DataFrame(comparison)

    new_table.plot(kind = 'bar', x='state', y='perc', title='Total transition - self loops ratio per state', color = '#3A9282', width=0.9)
    # plt.show()
    print("Sink states: ", sink_states)
    return sink_states

# Lists all the events which bring me to a sink states in order to extract their description from the event table.
def eventsToSinkStates(queryStatiEventi, queryEventi, sink_states, table1, table2):
    df = getDataframe(queryStatiEventi, table1)
    toSinkEvents = []
    for state in sink_states:
        array = df.query("(CURSTATE != @state) & (NEWSTATE ==  @state)")['IDEVENTO'].unique()
        for element in array:
            toSinkEvents.append(element)
    print("Event which bring to sink states: ", toSinkEvents)
    event_df = pd.DataFrame(queryEventi)
    event_df.columns = getDataframe(queryEventi, table2).columns
    selected_rows = event_df.loc[event_df['CCDOEV'].isin(toSinkEvents), ['CCDOEV', 'CDESCR']]
    print(selected_rows)

#Allows to get all the duplicate rows in a table
def duplicateSearch(queryRes, table):
    df = getDataframe(queryRes, table)
    if('NUMPRV' in df.columns.to_list()):
        df = df.drop('NUMPRV', axis=1)
    duplicated_rows = df[df.duplicated()]
    if(len(duplicated_rows.values.tolist())>0):
        print(duplicated_rows)
    else:
        print("Empty dataframe")

#Allows to understand if there are as many attribute's value as rows in the table
def numprvCoverage(queryRes, table, attr):
    df = getDataframe(queryRes, table)
    if(df.shape[0] == df[attr].max()):
        print(attr, "has a unique value for each rowin the dataframe")
    elif (df.shape[0] > df['NUMPRV'].max()):
        print(attr, "is not an unique identifier")
    elif (df.shape[0] < df['NUMPRV'].max()):
        print(attr, "is an unique identifier but it skip some row values")

#Allows to get the outcome of a process from an event (2E or O2). Those are the only ones where we can infer the outcome from the label associated with the event
def outcomeFromEventDescription(queryRes):

    dictionary = {}
    dictionary['rigetto'] = 0
    dictionary['accoglimento'] = 0
    dictionary['conferma'] = 0
    dictionary['rigetto'] = 0
    dictionary['riforma parziale'] = 0
    dictionary['riforma totale'] = 0
    dictionary['rinvio al primo grado'] = 0
    dictionary['accoglimento parziale'] = 0
    dictionary['accoglimento totale'] = 0
    dictionary['inammissibile'] = (extract(myconnection, query6, None)[0])[0]
    dictionary['n/a'] = 0
    dictionary['altro'] = 0

    print("Outcome for '2E' and 'O2' events: \n\n")
    for tuple in queryRes:
        if("ESITO" in tuple[1]):
            splittedString = tuple[1].split("ESITO")[1][:-1].strip().lower()
            if splittedString in dictionary.keys():
                dictionary[splittedString] +=1
            else:
                dictionary['altro'] += 1

        if ("NUMERO" in tuple[1]):
            splittedString = (tuple[1].split("NUMERO")[1])
            if( "(" in splittedString):
                splittedString = splittedString.split("(")[1][:-1].strip().lower()
                if splittedString in dictionary.keys():
                    dictionary[splittedString] += 1
                else:
                    dictionary['altro'] += 1

    for chiave, valore in dictionary.items():
        print(f"{chiave}: {valore}")

#Allows to get the distrubution of the value for those attribute. We want to infer if it's true that when RIFORMATA is full then CTIPOS has the same value as suggested by previous studies
def riformataVsCtiposDomain(queryRes, table):
    riformatadf = getDataframe(queryRes, table)['RIFORMATA']
    print("Value in RIFORMATA distribution:\n")
    print(riformatadf.value_counts(dropna=False).reset_index())

    ctiposdf = getDataframe(queryRes, table)['CTIPOS']
    print("\n\nValue in CTIPOS distribution:\n")
    print(ctiposdf.value_counts(dropna=False).reset_index())

# Allows to say if the statement "when Riformata is full Ctipos has the same value" suggested is true or not
def whenRiformataFullCtiposSameVal(queryRes, table):
    df = getDataframe(queryRes, table)[['NUMPRV', 'CTIPOS', 'RIFORMATA']].dropna()
    notTrueList = []
    for index, row in df.iterrows():
        if(row['RIFORMATA'] != row['CTIPOS']):
            notTrueList.append(row['NUMPRV'])
    print("It's not true that when Riformata is full Ctipos has the same value.", len(notTrueList), "examples says the opposite.")

#Allows to get the description of the most frequent 10 events in the stor table marked with each of the letter that RIFORMATA and CTIPOS could have
def lettersMeaning():
    dictionary = {}
    dictionary['rigetto'] = 0
    dictionary['accoglimento'] = 0
    dictionary['conferma'] = 0
    dictionary['rigetto'] = 0
    dictionary['riforma parziale'] = 0
    dictionary['riforma totale'] = 0
    dictionary['rinvio al primo grado'] = 0
    dictionary['accoglimento parziale'] = 0
    dictionary['accoglimento totale'] = 0
    dictionary['n/a'] = 0
    dictionary['altro'] = 0

    lettersArray = ['A', 'B', 'C', 'D', 'E', 'R', 'Z']
    print("##############################################################")

    for letter in lettersArray:
        print("\nWhen a dossier is marked with RIFORMATA =", letter, "the outcomes distribution looks like this:")
        joinedTable = extract(myconnection, query8, (letter, ))
        dictionary = {chiave: 0 for chiave in dictionary}

        for tuple in lastOutcomePerProcess(joinedTable):
            if("ESITO" in tuple[1]):
                splitted = tuple[1].split("ESITO")[1][:-1].strip().lower()
                if splitted in dictionary.keys():
                    dictionary[splitted]+=1

        for chiave, valore in dictionary.items():
            print(f"{chiave}: {valore}")

        keys_with_value = [key for key, value in dictionary.items() if value == max(dictionary.values())]
        print("Due to RIFORMATA analysis", letter, "seems to be related to", keys_with_value, "outcome")

        print("------------------------------------------------------------")
        print("\nWhen a dossier is marked with CTIPOS =",letter, "the outcomes distribution looks like this:")
        joinedTable = extract(myconnection, query9, (letter, ))
        dictionary = {chiave: 0 for chiave in dictionary}
        for tuple in lastOutcomePerProcess(joinedTable):
            if("ESITO" in tuple[1]):
                splitted = tuple[1].split("ESITO")[1][:-1].strip().lower()
                if splitted in dictionary.keys():
                    dictionary[splitted]+=1


        for chiave, valore in dictionary.items():
            print(f"{chiave}: {valore}")
            
        keys_with_value = [key for key, value in dictionary.items() if value == max(dictionary.values())]
        print("Due to CTIPOS analysis", letter, "seems to be related to", keys_with_value, "outcome")

        print("##############################################################")

#Allows to consider only the last occurrence of an outcome event in the same process in order to avoid corrections which multiply the number of events
def lastOutcomePerProcess(joinedTable):
    result = []
    index = 0
    while index < len(joinedTable):
        current_tuple = joinedTable[index]
        if index == len(joinedTable) - 1 or current_tuple[0] != joinedTable[index + 1][0]:
            result.append(current_tuple)
        index += 1
    return result

#Print the result of the query giving also some percentages
def correctionEventsCounter(correctionCount, rowCount):
    rowCountDf = pd.DataFrame(rowCount)
    totalRows = rowCountDf.shape[0]
    corrections = len(correctionCount)
    percentage = (corrections/totalRows) * 100
    print("The number of events in the stor table with 'correction' in their description is: ", corrections, "which is the: ", round(percentage, 2), "% of total rows in stor table")

#Allows to discover if all the correction events generate a self loop or if there are some of them which produces a flow deviation
def flowDeviationDiscovery(queryRes):
    deviatedNodes = []
    for tuple in queryRes:
        if(tuple[1]!=tuple[2]):
            deviatedNodes.append(tuple)
            #selects the correction events which are not C9 and are not self loops

    if(len(deviatedNodes)>0):
        print("The number of deviated nodes is: ", len(deviatedNodes))
        return deviatedNodes
    else: print("\nThe flow doesn't change when a correction event occurs")

#Allows to count the occurrences of a specific event giving also some percentages. Used to count the occurrences of the correction event C9, the only one that surely generates a flow deviation
def specificEventCounter(eventCount, rowCount, event):
    rowCountDf = pd.DataFrame(rowCount)
    totalRows = rowCountDf.shape[0]
    eventOcc = (eventCount[0])[0]
    percentage = (eventOcc/totalRows) * 100
    print("The number of", event ,"events in the stor table is: ", eventOcc, "which is the: ", round(percentage, 2), "% of total rows in stor table")

#Allows to subset the table and repet the flow deviation discovering excluding from the analysis all the events marked with C9
def flowDeviationDiscoverySubsetted(queryRes):
    subsetLen = pd.DataFrame(queryRes).shape[0]
    print("The total number of correction events which are not C9 (survived events) are: ", subsetLen)
    survived = flowDeviationDiscovery(queryRes)
    survivedCorrectionDescribe(survived)
    return survived

# Allows to describe the subset obtained
def survivedCorrectionDescribe(result):
    print("Rituality correction event occurrencies: ")
    df = pd.DataFrame(result)
    dictionary = {}
    dictionary['CORREZIONE RITUALITA'] = 0
    dictionary['ALTRO'] = 0
    
    for survived in result:
        if(survived[3].find('RITO')!=-1 or survived[3].find('RITUALIT')!=-1):
                dictionary['CORREZIONE RITUALITA']+=1
        else: dictionary['ALTRO']+=1

    for chiave, valore in dictionary.items():
        print(f"{chiave}: {valore}")

# Allows to describe the structure of the dataset after deleting the rite corrections. We want to descover the nature of correction events which are not state changes or rituality changes
def survivedNotRiteCorrectionDescribe(result):
    print("Neither c9 nor rituality correction events description: ")
    df = pd.DataFrame(result)
    dictionary = {}
    dictionary['CORREZIONE ERRORE MATERIALE'] = 0
    dictionary['DATI FASCICOLO CORRETTI'] = 0
    dictionary['DATI GRADO PRECEDENTE CORRETTI'] = 0
    dictionary['ALTRO'] = 0
    
    count = 0
    for survived in result:
        if ("rito" not in survived[3].lower()):
            if(survived[3].find('CORREZIONE ERRORE MATERIALE')!=-1):
                dictionary['CORREZIONE ERRORE MATERIALE']+=1
            elif(survived[3].find('DATI FASCICOLO CORRETTI')!=-1):
                dictionary['DATI FASCICOLO CORRETTI']+=1
            elif(survived[3].find('DATI GRADO PRECEDENTE CORRETTI')!=-1):
                dictionary['DATI GRADO PRECEDENTE CORRETTI']+=1
            elif(survived[3].find('DATI FASCICOLO CORRETTI')==-1 and survived[3].find('CORREZIONE ERRORE MATERIALE')==-1 and survived[3].find('DATI GRADO PRECEDENTE CORRETTI')==-1): 
                dictionary['ALTRO']+=1
            count+=1

    for chiave, valore in dictionary.items():
        print(f"{chiave}: {valore}")

#Prints the rows of stor containing 'rito' or 'ritualita' in the event description to infer their ccdoev
def printRowContainingRit(queryRes):
    for tuple in queryRes:
        print(tuple)

#Return the frequency of each event involving rites
def ritualityChanges(queryRes):
    print("The total number of rituality involving event is: ", pd.DataFrame(queryRes).shape[0])
    keyList = [
    ('PC', 'PASSAGGIO AL RITO ORDINARIO'),
    ('QN', 'MUTAMENTO RITO E ISCRIZIONE CAUSA ORDINARIA'),
    ('OG', 'ORDIN. DI CON. SFRATTO + MODIF. RITO + FISS. UDIE.'),
    ('OU', 'ORDINANZA DI RILASCIO, MODIFICA RITO E ISCRIZIONE CAUSA ORDINARIA'),
    ('MU', 'MODIFICA RITO E FISSAZIONE UDIENZA'),
    ('MR', 'MODIFICA RITO'),
    ('N2', 'MUTAMENTO RITO CON FISSAZIONE UDIENZA'),
    ('GB', 'MUTAMENTO A RITO SOCIETARIO ORDINARIO DI COGNIZIONE'),
    ('GO', 'MUTAM. A RITO ORDINARIO, DESIGN. GIUDICE E FISSAZIONE UDIENZA (art.16 6^C)'),
    ('GP', 'MUTAM. A RITO ORD, RIMESS. GIUDICE COMPETENTE E FISSAZ. TERMINE PER DEP.RICORSO '),
    ('H7', 'MUTAMENTO A RITO ORDINARIO SOCIETARIO'),
    ('HC', 'MUTAMENTO RITO E RIMESSIONE AL PRESIDENTE DEL TRIBUNALE'),
    ('HD', 'MUTAMENTO A RITO ORDINARIO E ASSEGNAZIONE A SEZIONE'),
    ('C0', 'CORREZIONE RITUALITA`'),
    ('5G', 'MUTAMENTO A RITO ORDINARIO EX ART. 427 CPC (iscrizione fascicolo)'),
    ('5T', 'MUTAMENTO A RITO ORDINARIO E FISSAZIONE UDIENZA ex art. 180'),
    ('5Z', 'MUTAMENTO A RITO ORDINARIO E FISSAZIONE UDIENZA ex art. 183'),
    ('3D', 'RIGETTO ISTANZA, MUTAMENTO RITO E ISCRIZIONE CAUSA ORDINARIA'),
    ('3N', 'PAGAMENTO CONDIZIONATO,MUTAMENTO RITO E ISCR. CAUSA ORDINARIA (art.55 L.392/78)'),
    ('3P', 'VERIFICA  PAGAMENTO SOMME NON CONTESTATE E MUTAMENTO RITO (art.666 cpc)'),
    ('4K', 'MODIFICA RITO (EX ART. 669 NOVIES CPC)'),
    ('04', 'MUTAMENTO A RITO SOCIETARIO ORDINARIO DI COGNIZIONE')
    ]

    for key in keyList:
        count = 0
        for change in queryRes:
            if(change[0] == key[0]):
                count += 1
        print(count, "occurrences for rituality with id: ", key[0], "and description: ", key[1])

#Display from which rite to which oter we jump when a 'correzione ritualità' event occurs
def showC0Changes(queryRes):
    ritualFromTo = []

    for element in queryRes:
        separatedValues = element[0].split(";")
        tuple = (separatedValues[0], separatedValues[1])
        ritualFromTo.append(tuple)

    labels = []
    measures = []

    for index in range(0, len(ritualFromTo)-1):
        count = 1
        for secondIndex in range(index+1, len(ritualFromTo)-1):
            if(ritualFromTo[index] == ritualFromTo[secondIndex]):
                count+=1

        if(count>10 and ritualFromTo[index] not in labels):
            labels.append("(" + (ritualFromTo[index])[0] + "/" + (ritualFromTo[index])[1] + ")")
            measures.append(count)


    plt.xlabel('Rituality changes', fontsize= 10)
    plt.xticks(fontsize=8)
    plt.gca().yaxis.set_major_locator(MultipleLocator(25))

    plt.bar(labels, measures, color = '#3A9282', width=0.5)
    plt.show()

# Plot the distribution of every value of IDGRPEV
def plotIDGRPEV(distinctAttr, allAttr):
    labels = []
    measures = []

    for distinctel in distinctAttr:
        count = 1
        for el in allAttr:
            if distinctel == el:
                count += 1
        labels.append(distinctel[0])
        measures.append(count)

    plt.xlabel('Distribution of IDGRPEV occurrences', fontsize= 10)
    plt.xticks(fontsize=8)
    plt.bar(labels, measures, color = '#3A9282', width=0.5)
    plt.show()
    return labels

# Print the description of the 10 most frequent event associate with the IDGRPEV under test
def inferMeaning(QueryRes, labels):
    #0) Gather in a dataframe all the event in the stor table
    df = pd.DataFrame(QueryRes, columns=["CCDOEV"])
    listOfLists = []
    # most frequent IDGRPEV for 4O rituality:
    interestingLabels = [labels[0], labels[2], labels[56], labels[3], labels[43], labels[37], labels[35]]
    #index of interestingLabels

    i=0
    for labels in interestingLabels:
        #1) Gather in a list all the events which codify for an unique IDGRPEV (PP in this case)
        toSearch = []
        eventsForinStaEv = extract(myconnection, query20, (interestingLabels[i], ))
        for tuple in eventsForinStaEv:
            if tuple[0] not in toSearch:
                toSearch.append(tuple[0])
        #2) Gather in a list of list all the results
        listOfLists.append(toSearch)
        i+=1
    #3) Select in the dataframe with all the events just the ones which codify for an unique IDGRPEV which is a particular list in the listoflists
    i=0
    for toSearch in listOfLists:
        eventsinStor = df.query("(CCDOEV in @toSearch)")

    #4) Sort it according to the number of occurrences of each event in the stor table and select just the 10 most frequent event code
        print("----------------------------------------")
        print("Most frequent event for IDGRPEV:, ", interestingLabels[i], "count: ")
        mostFreqEv = eventsinStor['CCDOEV'].value_counts().head(10)
        print(mostFreqEv)
        print("\n")

    #5) Associate the code with the decription of the event
        allFromEventi = extract(myconnection, query21 , None)
        print("Most frequent event for IDGRPEV, ", interestingLabels[i], " description: ")
        df = pd.DataFrame(allFromEventi, columns=["CCDOEV", "DESCR"])
        keys_list = list(mostFreqEv.to_dict().keys())
        eventsdescr = df.query("(CCDOEV in @keys_list)")
        eventsdescr = eventsdescr.reset_index(drop=True)
        print(eventsdescr)
        print("\n")
        print("----------------------------------------")

        ccdoev = extract(myconnection, query19, None)
        df = pd.DataFrame(ccdoev, columns=["CCDOEV"])
        i+=1

# Write a text file formatting the result returned from the query in a way easy to work on for the iteronfile function
def verticalConsistencyCheck(queryRes):
    with open('eventOccurrence.txt', 'w') as file:
        # file.write("The file was successfully created.\n\n")
        count = 1
        for rows in queryRes:
            dossier = rows[0]
            date = rows[1]
            if(dossier!=count):
                count+=1
                file.write("\n")
            file.write(f"{date} ")

    iterOnFile('eventOccurrence.txt')

# Reads the file and detects vertical temporal inconsistencies
def iterOnFile(fileName):
    numberDossier = 0
    with open (fileName, 'r') as file:
        for dossier in file:
            numberDossier+=1
            dateStringSineNewline = dossier.strip().split(' ')
            for string in dateStringSineNewline:
                datetime.strptime(string, "%Y-%m-%d").date()
            for i in range(len(dateStringSineNewline)-1):
                if(dateStringSineNewline[i]>dateStringSineNewline[i+1]):
                    print("In dossier: ", numberDossier,  " this couple of events -> string[i]: ", dateStringSineNewline[i], ", string[i+1]: ", dateStringSineNewline[i+1], " are not temporally sorted")

# Write a text file formatting the result returned from the query in a way easy to work on for the iteronfile2 function
def horizontalConsistencyCheck(queryRes):
    with open('eventConsistency.txt', 'w') as file:
        for tuple in queryRes:
            dossier = tuple[0]
            dateEvent = datetime.combine(tuple[1], datetime.min.time())
            dateReg = tuple[2]
            dateMod = tuple[3]
            numprv = tuple[4]
            file.write(f"{dossier},{dateEvent},{dateReg},{dateMod},{numprv}\n")

    iterOnFile2('eventConsistency.txt')

# Reads the file and detects where occurrence date < registration date < modification date working horizontally on stor table rows
def iterOnFile2(fileName):
    with open (fileName, 'r') as file:
        for row in file:
            tupleList = row.strip().split(',')
            dateEvent = datetime.strptime(tupleList[1], '%Y-%m-%d %H:%M:%S')
            dateReg = datetime.strptime(tupleList[2], '%Y-%m-%d %H:%M:%S')
            dateMod = datetime.strptime(tupleList[3], '%Y-%m-%d %H:%M:%S')
            numpro = tupleList[0]
            numprv = tupleList[4]

            if(dateEvent > dateReg): print("In log with numprv:", numprv, " and dossier: ", numpro, "The occurrence of event follows its registration")
            if(dateEvent > dateMod): print("In log with numprv:", numprv, " and dossier: ", numpro , " The occurrence of event follows its modification")
            if(dateReg > dateMod): print("In log with numprv:", numprv, "  and dossier: ", numpro, "The registration of event follows its modification")

# Detects rows where the same event (same ccdoev and same occurrence day) seeems to have multiple registration dates and for each of them a different lastModificationDate
def sameDayDifferentRegOrMod(queryRes):
    for duplicateRows in queryRes:
        print("Tabel: stor, in dossier: ", duplicateRows[0], "and cdescr: ", duplicateRows[7], "presents different modification or registration time for the same event")
    print("The number of duplicate rows is: " , len(queryRes))

# We were searching for different version of the stati eventi table released in differnent times in order to lead an analysis on isVisible meaning. So we tried to compare the only two versions of stati eventi that we had.
def areTheSameTable(queryRes):
    # We print the difference between the two tables
    print(queryRes)

# Investigate if there are events which are marked as invisible in state event table but actually appear in some logs. Useful to see if invisibility implies no more occurrence in logs. Of course all depends on the date in which they are mafe invisible (we lack this information!)
def invisibilityDiscovery (invisibleEvent, history):
    for event in invisibleEvent:
        for log in history:
            if(event[0] == log[1]):
                print("There are events which are marked as invisible in state event table but actually appear in some logs")
                return
    print("There are not events which are marked as invisible in state event table but actually appear in some logs")

#Print a matrix that displays how many times there's a match between the value in RIFORMATA and in CTIPOS and how many times a mismatch occurrs
def printMatrix(queryRes):

    matrix = np.zeros((8, 8), dtype=int)

    def convert(letter):
        match letter:
            case "A": return 0
            case "B": return 1
            case "C": return 2
            case "D": return 3
            case "E": return 4
            case "R": return 5
            case "Z": return 6
            case None : return 7
            case _: raise ValueError(f"Unexpected letter: {letter}")

    counter = 0

    for entry in queryRes:
        if(entry[0] == None):
            counter+=1

        riformata, ctipos = entry
        r_index = convert(riformata)
        c_index = convert(ctipos)
        
        if r_index is None or c_index is None:
            raise ValueError(f"Conversion returned None for entry: {entry}")
        matrix[r_index][c_index] += 1
    
    for rows in matrix:
        print(rows)

    print(counter)
    print(len(queryRes))

#Compare the value of riformata and ctipos with the description of the event in the stor table
def compareDescription():
    outcomes = ['%Accoglimento%', '%Rigetto%', '%Conferma%', '%Riforma parziale%', '%Riforma totale%', '%Rinvio al primo grado%', '%Altro%']
    riformataVal = ['A', 'B', 'C', 'D', 'E', 'R', 'Z']
    ctiposVal = ['A', 'B', 'C', 'D', 'E', 'R', 'Z']
    result= []

    for element in outcomes:
        print("ELEMENT: ", element)
        for letter in riformataVal:
            print("RIFORMATA: ", letter)
            for tipos in ctiposVal:
                queryRes = extract(myconnection, query29, (element , letter, tipos))
                result.append(len(queryRes))
                print(result[len(result)-1])

    # print(result)
    print("\n\nWhat if we have null value in ctipos?\n\n")

    result1 = []
    for element in outcomes:
        for letter in riformataVal:
            queryRes = extract(myconnection, query30, (element , letter))
            result1.append(len(queryRes))
    print(result1)
    print("\n\nWhat if we have null value in riformata?\n\n")

    result2 = []
    for element in outcomes:
        for letter in riformataVal:
            queryRes = extract(myconnection, query31, (element , letter))
            result2.append(len(queryRes))
    print(result2)
    print("\n\nWhat if we have null value in riformata and ctipos?\n\n")

    result3 = []
    for element in outcomes:
            queryRes = extract(myconnection, query32, (element,))
            result3.append(len(queryRes))
    print(result3)



#QUERIES DEFINITION AREA

query0 = """
SELECT *
FROM Database.statievento
"""
query1 = """
SELECT *
FROM Database.statievento
WHERE ritualita = '4O'
"""
query2 = """
SELECT *
FROM Database.eventi
"""
query3 = """
SELECT *
FROM Database.stor
"""
query4 = """
SELECT *
FROM Database.fasc
"""
query5 = """
SELECT numpro, cdescr
FROM database.stor
WHERE ccdoev ='2E' or ccdoev ='O2'
"""
query6 = """
SELECT count(*)
FROM database.stor
WHERE ccdoev ='IS'
"""
query7 = """
SELECT *
FROM database.defi
"""
query8 = """
SELECT stor.numpro, stor.cdescr
FROM Database.stor as stor  join database.defi as defi on stor.numpro = defi.numpro
WHERE defi.riformata = %s and stor.cdescr like '%ESITO%'
ORDER BY stor.numpro ASC
"""
query9 = """
SELECT stor.numpro, stor.cdescr
FROM Database.stor as stor  join database.defi as defi on stor.numpro = defi.numpro
WHERE defi.ctipos = %s and stor.cdescr like '%ESITO%'
ORDER BY stor.numpro ASC
"""
query10 = """
SELECT distinct numprv
FROM Database.stor AS stor
WHERE stor.ccdoev = any(
    SELECT eventi.ccdoev
    FROM Database.eventi AS eventi
    WHERE eventi.cdescr LIKE 'Correzione%' or eventi.cdescr LIKE '%correzione%')
"""
query11 = """
SELECT distinct numprv, cstapr, ccodst
FROM Database.stor AS stor
WHERE stor.ccdoev = any(
    SELECT eventi.ccdoev
    FROM Database.eventi AS eventi
    WHERE eventi.cdescr LIKE 'Correzione%' or eventi.cdescr LIKE '%correzione%')
"""
query12 = """
SELECT count(*)
FROM Database.stor
WHERE ccdoev = %s
"""
query13 = """
SELECT distinct numprv, cstapr, ccodst, cdescr
FROM Database.stor AS stor
WHERE
stor.ccdoev <> %s AND
stor.ccdoev = any(
    SELECT eventi.ccdoev
    FROM Database.eventi AS eventi
    WHERE eventi.cdescr LIKE 'Correzione%' or eventi.cdescr LIKE '%correzione%')
"""
query14 = """
SELECT CCDOEV, CDESCR
FROM database.eventi
WHERE cdescr LIKE '%rito%' or cdescr LIKE '%ritualit%'
"""
query15 = """
SELECT ccdoev
FROM database.stor
WHERE ccdoev = 'PC' or ccdoev = 'QN' or ccdoev = 'OG' or ccdoev = 'OU' or ccdoev = 'MU' or ccdoev = 'MR' or ccdoev = 'N2' or ccdoev = 'GB' or ccdoev = 'GO' or ccdoev = 'GP' or ccdoev = 'H7' or ccdoev = 'HC' or ccdoev = 'HD' or ccdoev = 'C0' or ccdoev = '5G' or ccdoev = '5T' or ccdoev = '5Z' or ccdoev = '3D' or ccdoev = '3P' or ccdoev = '4K' or ccdoev = '04'
"""
query16 = """
SELECT cnpara
FROM database.stor
WHERE ccdoev = 'C0' and cnpara is not null
"""
query17 = """
SELECT distinct idgrpev
FROM Database.statievento
WHERE idgrpev <> '-'
"""
query18 = """
SELECT idgrpev
FROM Database.statievento
WHERE idgrpev <> '-'
"""
query19 = """
SELECT ccdoev
FROM database.stor
"""
query20 = """
SELECT idevento
FROM database.statievento
WHERE idgrpev = %s
"""
query21 = """
SELECT CCDOEV, CDESCR
FROM database.eventi
"""
query22 = """
SELECT numpro, dataev
FROM database.stor
GROUP BY numpro, dataev
"""
query23 = """
SELECT numpro, dataev, datare, dataultimamodifica, numprv
FROM database.stor
GROUP BY numpro, dataev, datare, dataultimamodifica, numprv
"""
query24 = """
SELECT NUMPRO, CCDOEV, CTIPSE, NUMGIU, DATAEV, CCODST, CNPARA, CDESCR, CODUTE, CEVPAD, CSTAPR, ISVISIBLE, CRONOLOGICO, IDTIPOATTOCRONOLOGICO, PARAMS, NOTA, IDDOCS
FROM database.stor
GROUP BY NUMPRO, CCDOEV, CTIPSE, NUMGIU, DATAEV, CCODST, CNPARA, CDESCR, CODUTE, CEVPAD, CSTAPR, ISVISIBLE, CRONOLOGICO, IDTIPOATTOCRONOLOGICO, PARAMS, NOTA, IDDOCS
HAVING COUNT(*) > 1
"""
query25 = """
SELECT isvisible
FROM Database.statievento
EXCEPT
SELECT isvisible
FROM stati_eventi.statievento;
"""
query26 = """
SELECT idevento
FROM Database.statievento
WHERE isvisible = 0
"""
query27 = """
SELECT numprv, ccdoev
FROM Database.stor
"""
query28 = """
SELECT defi.riformata, defi.ctipos
FROM Database.stor as stor  join database.defi as defi on stor.numpro = defi.numpro
"""
query29 = """
SELECT defi.numpro, defi.riformata, defi.ctipos, stor.cdescr 
FROM Database.defi as defi join Database.stor as stor on defi.numpro = stor.numpro
WHERE stor.cdescr LIKE %s
AND (stor.ccdoev = "2E" or stor.ccdoev = "O2")
AND (defi.riformata = %s)
AND (defi.ctipos = %s)
;
"""
query30 = """
SELECT defi.numpro, defi.riformata, defi.ctipos, stor.cdescr 
FROM Database.defi as defi join Database.stor as stor on defi.numpro = stor.numpro
WHERE stor.cdescr LIKE %s
AND (stor.ccdoev = "2E" or stor.ccdoev = "O2")
AND (defi.riformata = %s)
AND (defi.ctipos is null)
;
"""
query31 = """
SELECT defi.numpro, defi.riformata, defi.ctipos, stor.cdescr 
FROM Database.defi as defi join Database.stor as stor on defi.numpro = stor.numpro
WHERE stor.cdescr LIKE %s
AND (stor.ccdoev = "2E" or stor.ccdoev = "O2")
AND (defi.riformata is null)
AND (defi.ctipos = %s)
;
"""
query32 = """
SELECT defi.numpro, defi.riformata, defi.ctipos, stor.cdescr 
FROM Database.defi as defi join Database.stor as stor on defi.numpro = stor.numpro
WHERE stor.cdescr LIKE %s
AND (stor.ccdoev = "2E" or stor.ccdoev = "O2")
AND (defi.riformata is null)
AND (defi.ctipos is null)
;
"""



#MAIN

myconnection = enstablishConnection("localhost", "root", "ZAQ1!qaz", "Database")

# XXX Exploratory phase:

# describeTable(extract(myconnection, query0, None), 'statievento')
# describeTable(extract(myconnection, query1, None), 'statievento')
# describeTable(extract(myconnection, query3, None), 'stor')
# loopsTransactionsGlobalCount(extract(myconnection, query0, None), 'statievento')

# duplicateSearch(extract(myconnection, query3, None), 'stor')
# duplicateSearch(extract(myconnection, query4, None), 'fasc')

# numprvCoverage(extract(myconnection, query3, None), 'stor', 'NUMPRV')

# XXX Meaning infer IDGRPEV

# plotAttributeDistr(extract(myconnection, query0, None), "IDGRPEV", 'statievento')
# labels = plotIDGRPEV(extract(myconnection, query17, None), extract(myconnection, query18, None))
# inferMeaning(extract(myconnection, query19, None), labels)

# XXX Final states analysis

# sink_states = loopsTransactionsLocalCount(extract(myconnection, query0, None), 'statievento')
# eventsToSinkStates((extract(myconnection, query0, None)),(extract(myconnection, query2, None)), sink_states, 'statievento', 'eventi')

# sink_states = loopsTransactionsLocalCount(extract(myconnection, query1, None), 'statievento')
# eventsToSinkStates((extract(myconnection, query1, None)),(extract(myconnection, query2, None)), sink_states, 'statievento', 'eventi')

# outcomeFromEventDescription(extract(myconnection, query5, None))
# riformataVsCtiposDomain(extract(myconnection, query7, None), 'defi')
# whenRiformataFullCtiposSameVal(extract(myconnection, query7, None), 'defi')
# lettersMeaning()
# printMatrix(extract(myconnection, query28, None))
compareDescription()

# XXX Correction event analysis

# correctionEventsCounter(extract(myconnection, query10, None), extract(myconnection, query3, None))
# flowDeviationDiscovery(extract(myconnection, query11, None))
# specificEventCounter(extract(myconnection, query12, ('C9',)), extract(myconnection, query3, None), 'C9')

# survived = flowDeviationDiscoverySubsetted(extract(myconnection, query13, ('C9',)))
# survivedNotRiteCorrectionDescribe(survived)

# XXX Rituality switches

# printRowContainingRit(extract(myconnection, query14, None))
# ritualityChanges(extract(myconnection, query15, None))
# showC0Changes(extract(myconnection, query16, None))

# XXX Timelines inconsistencies

# verticalConsistencyCheck(extract(myconnection, query22, None))
# horizontalConsistencyCheck(extract(myconnection, query23, None))
# sameDayDifferentRegOrMod(extract(myconnection, query24, None))

# XXX isVisible analysis

# plotAttributeDistr(extract(myconnection, query0, None), "ISVISIBLE, 'statievento'")
# areTheSameTable(extract(myconnection, query25, None))
# invisibilityDiscovery(extract(myconnection, query26, None), extract(myconnection, query27, None))