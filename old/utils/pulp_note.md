### Documentazione sulla libreria Pulp ###
__Nota__: la libreria è già automaticamente caricata in questo foglio tramite il comando _import pulp as p_.

__Metodi disponibili__:
- probLp = p.LpProblem(prob\_name, obj): definisce un nuovo problema di Programmazione Lineare _probLp_ , dandogli il nome _prob\_name_ e impostando l'obiettivo _obj_ (che può essere p.LpMinimize o p.LpMaximize);
- p.LpVariable(var\_name): aggiunge una variabile di nome _var\_name_ al problema; questo metodo ha vari parametri opzionali che possono aggiungersi (e.g., lowBound, upBound, cat);
- probLp += expression: aggiunge un vincolo o la funzione obiettivo, rappresentati da _expression_ , al problema _probLp_ ;
- status = probLp.solve(): risolve il problema _probLp_ , ritornando informazioni sullo _status_ ;
- p.value(var\_name): ritorna il valore della variabile _var\_name_ .


Per maggiori informazioni, consultare la [documentazione ufficiale](https://www.coin-or.org/PuLP/pulp.html).
