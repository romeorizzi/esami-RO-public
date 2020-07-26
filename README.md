Questa repo (esami-RO-public) contiene gli script per generare il tema d'esame personale per ciascun studente iscritto all'appello.
In realtà il singolo appello viene generato entro una repo gemella (esami-RO-private) ma la presente repo mira a dare la massima trasparenza al processo di generazione non solo per condividere in modo chiaro con gli studenti quali siano le competenze che dovranno esprimere all'esame ma anche per condividere con loro l'opportunità di progetti utili al corso.
Alcuni esercizi che necessitassero di maggior protezione (per fragilità strutturale o perchè sempre vorremo anche in futuro continuare ad introdurre anche delle novità) compariranno in questa repo solo ad esame avvenuto. Questa repo offre la base di dati sulla quale poggia il servizio di simulazione di un esame del passato, è sarà quindi completata dove necessario a valle di ogni appello.
Pertanto, lo studente può a pieno diritto considerarla come l'officina dove è stato costruito l'appello.

Ogni tema d'esame personale viene ad essere costituito pescando un diverso esercizio disponibile da ciascuna tipologia prevista per l'appello.
Nella gestione di un appello si parte cioè da una collezione di esercizi già finalizzati (cablati su una specifica istanza già determinata e finalizzati già in ogni aspetto) e ripartiti in cartelle e sottocartelle in base alla tipologia.
Questa repo pubblica non contiene la cartella degli esercizi di un appello fino a dopo l'appello, ma sempre più nel tempo conterrà dei generatori generali per alcune tipologie di esercizio (quelle che si sono affermate nel tempo e dove è stato possibile approntare generatori con tali caratteristiche).

In realtà il meccanismo di generazione degli esercizi deve avvanire in due fasi, dove le cartelle del paragrafo precedente sono il punto di arrivo della prima fase ed il punto di partenza della seconda. In questo paragrafo cerchiamo di chiarire questo ed il suo perchè.
Il meccanismo di selezione dell'esercizio entro la sua tipologia richiede l'informazione della matricola dello studente e della data dell'appello.
Date queste due informazioni l'esercizo deve uscirne determinato, come necessario per il servizio di simulazione di un appello del passato.
Non vogliamo però che lo studente possa prevedere prima dell'appello il suo esercizio per una data tipologia nemmeno se egli già conosce o può ipotizzare i generatori per quella tipologia, che dove possibile ci piace rendere disponibili in questo repo pubblico anche per la valenza didattica e formativa del condividere e collaborare su questi materiali. Considerato inoltre che vogliamo gestire anche lo studente che aveva dimenticato di iscriversi all'appello, e che altri imprevisti sono sempre possibili, abbiamo reputato più prudente e semplice ricorrere ad una generazione in due fasi:
nella prima fase vengono riempite le cartelle degli esercizi-cablati dell'appello, nella seconda fase viene composto il tema di ciascun studente.

Siamo ora pronti per introdurre un pizzico di terminologia: Distinguiamo tra esercizi-cablati (allo studente, per ciascuna tipologia, spetterà un esercizio cablato già determinato in ogni singola richiesta) ed esercizi-tipo (stampini per la generazione degli esercizi-cablati utilizzati nell'appello).

Ogni esercizio può prevedere più modalità di svolgimento e sottomissione, ma, una volta fissato lo studente e l'appello, il testo per quell'esercizio deve essere sostanzialmente equivalente al variare della modalità di svolgimento e sottoposizione.
I meccanismi che determinano la famiglia dei diversi esercizi disponibili di una data tipologia dipendono dalla tipologia stessa.
Alcuni esercizi-tipo, specie inizialmente nel loro percorso di vita, vengono coniugati manualmente ed ad-hoc in diverse versioni. (Anche in questo viene conveniente per robustezza e semplicità il meccanismo di generazione in due fasi.)
Altri trovano dei meccanismi di generazione automatica diretti, per altri gli esercizi generati automaticamente devono superare dei filtri di qualità. Alcuni esercizi-tipo prevedono strumenti che consentano l'esplorazione dei rispttivi esercizi-cablati. Specie per gli esercizi che richiedono una validazione più attenta, sono previsti meccanismi di generazione partendo da esercizi-cablati già valutati godere di proprietà auspicabili, tramite la produzione di esercizi ad essi equivalenti (sfruttando isomorfismi specifici all'esercizio-tipo in questione).
Il processo di generazione verrà ad essere maggiormente integrato ed affinato appello dopo appello. Attualmente, per alcuni problemi, Alice ha disposto nella cartella script_instances/  alcuni script di generazione del problema inclusa l'istanza di riferimento. Questi script nella cartella script_instances/ sono attualmente rivolti alla generazione di un file yaml spendibile per la sola modalità di sottomissione libera strutturata.
Ora Alessandro aggiungerà dei problemi dove viene ad essere generata la modalità entro foglio jupyter elementare ma con validatori a supporto.
Ed andrà ricercato come meglio mettere gli elementi a fattore comune per ottenere la generazione di entrambe le modalità a partire dagli stessi sorgenti (non ancora chiaro se meglio partire da istanza, o qualcosa di più, o qualcosa di meno).



# COME CREARE UN NUOVO TEMA D'ESAME DI RICERCA OPERATIVA PER L'APPELLO DEL YYYY-MM-DD

## Cartelle necessarie
1. __collection\_YYYY-MM-DD__: contenitore delle istanze possibili; contiene _n_ sottocartelle, una per ogni tipologia di esercizio che sarà inserita nel tema esame; ogni sottocartella deve contenere almeno un'istanza in formato .yaml; _n_ è anche il valore del parametro NB\_EXERCISES nello script _generate\_exam.py_;
2. __students\_list\_YYYY-MM-DD__: contiene dei file .csv con la lista degli studenti iscritti all'appello e le loro chiavi;
3. __img\_YYYY-MM-DD__: contiene le immagini necessarie ad alcune istanze di esercizi nella cartella _collection\_YYYY-MM-DD_;
4. __utils__: indispensabile per ogni generazione, non dipende dalla data dell'esame.

## Descrizione degli scripts:
- __generate\_all\_exams\_given\_list.py__: a partire dalla lista di studenti iscritti all'appello in data YYYY-MM-DD, riempie la cartella _shuttle_ con i temi d'esame corrispondenti, invocando per ogni studente lo script _generate\_exam.py_;
- __generate\_exam.py__: a partire dalla data d'esame e dalle informazioni anagrafiche di uno studente, genera la sua cartella contenente il tema d'esame compresso in due formati (.zip e .tgz); invoca _n_ volte gli script per generare gli esercizi come fogli Jupyter (2020-07-06: al momento chiama solo _create\_exercise\_free.py_ per aggiungere la modalità di sottomissione libera e strutturata);
- __create\_exercise\_free.py__: a partire dalle informazioni di un dato studente e dall'istanza scelta di una certa tipologia di esercizio, genera il singolo esercizio in modalità libera e strutturata;
- __create\_exercise\_verifier.py__: esercizi con verificatori (2020-07-06: non ancora implementato);
- __create\_exercise\_applet.py__: esercizi con applet (2020-07-06: non ancora implementato);
- __generate\_all\_instances\_given\_date.py__: script per generare, in un'unica cartella, tutti gli esercizi di una certa collezione relativa alla data passata come parametro.
- ___map\_generator.py__: funzione per generare la mappa (utilizza  i template html contenuti in /template)

## Per generare tutti i temi d'esame di una certa data:
`python generate_all_exams_given_list.py YYYY-MM-DD path_to_students_list.csv`

Check `python generate_all_exams_given_list.py -h` per informazioni più dettagliate sui parametri da passare (in tutti gli script è presente l'help).

### Altre cartelle presenti:
- __script\_instances__: contiene script per generare automaticamente nuove istanze (2020-07-06: al momento ci sono solo _dp\_poldo_ e _dp\_string_ (LCS)); ricevono come parametro la data dell'esame in formato YYYY-MM-DD, in modo da aggiungere i nuovi file alla cartella _collection\_YYYY-MM-DD_ corrispondente;
- __other\_exercises__: istanze di esercizi da controllare e/o sistemare.
- __map__: contiene i file necessari al funzionamento della mappa html che viene generata. Tali file verranno copiati in ogni esame.