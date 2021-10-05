### Documentazione sulla classe Tableau disponibile nella libreria del simplesso interattivo ###
__Nota__: la libreria è già automaticamente caricata in questo foglio.

__Metodi disponibili__:
- t = Tableau(n, m, obj, prob\_type, term\_noto\_obj): definisce un nuovo problema di programmazione lineare avente _n_ variabili e _m_ vincoli; _obj_ sono i coefficienti delle variabili nella funzione obiettivo; _prob\_type_ può essere 'max' o 'min'; _term\_noto\_obj_ è un parametro opzionale casomai nella funzione obiettivo ci sia un valore costante da aggiungere; il tableau è di tipo completo (i.e., mostra nelle colonne tutte le variabili, comprese le slack);
- t.aggiungi\_vincolo(expression, value): aggiunge un vincolo di disuguaglianza '<=' con coefficienti delle variabili i valori contenuti in _expression_ e termine noto _value_ ;
- t.is\_optimal(): restituisce True o False;
- t.is\_feasible(): restituisce True o False;
- t.mostra\_tableau(): stampa il tableau corrente;
- t.crea\_primo\_tableau(): una volta definito il problema e inseriti i vincoli, crea il primo tableau e la prima soluzione di base;
- t.step\_primale(): esegue un passo del simplesso primale sul tableau t;
- t.step\_duale(): esegue un passo del simplesso duale sul tableau t;
- t.pivot\_colonna\_riga(c,r): esegue un'operazione di pivot facendo entrare in base la variabile della colonna _c_ e facendo uscire la variabile della riga _r_ ;
- t.stampa\_soluzione\_base\_corrente();
- t.prossimo\_step(): sulla base della soluzione di base corrente, ritorna informazioni sulla feasibility e l'ottimalità e suggerisce il passo successivo da fare per la risoluzione del problema.
