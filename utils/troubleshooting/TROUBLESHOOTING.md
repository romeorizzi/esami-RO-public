# TROUBLESHOOTING - Errori comuni e come risolverli

__Indice__:
- A) Problemi durante lo svolgimento dell'esercizio
- B) Problemi con il salvataggio e l'esportazione del foglio in HTML

Se rilevate ulteriori issue non presenti su questo file, segnalateceli (magari allegando uno o più screenshot) mandando un'email agli indirizzi `romeo.rizzi@univr.it, alice.raffaele@univr.it`.

## A) Problemi all'apertura del foglio

1. __Trust Notebook__: all'apertura del foglio Jupyter potrebbe comparirvi il seguente messaggio:

![Figura: TrustNotebook](img/TrustNotebook.png)

Cliccando su `Trust notebook`, apparirà un altro messaggio:

![Figura: TrustNotebook2](img/TrustNotebook2.png)

Cliccare ancora su `Trust`. Ciò consentirà al foglio Jupyter di eseguire in automatico, ogni volta che lo aprirete, le celle che importano le librerie necessarie, visualizzando anche il tasto `Avvio esercizio`.

2. __Package mancanti__: dopo aver aperto il foglio Jupyter, potrebbero comparire messaggi del genere relativi a dei package che, per qualche motivo, non sono stati caricati nell'environment di ROexam.

Per esempio:
- pulp:

![Figura: Pulp-Issue1](img/Pulp-Issue1.jpg)

![Figura: Pulp-Issue2](img/Pulp-Issue2.png)

- ipysheet:

![Figura: IPysheet-Issue1](img/IPysheet-Issue1.jpg)

- numpy:

![Figura: Numpy-Issue1](img/Numpy-Issue1.png)

Per tutti questi casi, e analogamente per altri package, potete procedere in due modi:
1. Direttamente sul foglio Jupyter, aggiungere una cella di codice e digitare `! pip install --ignore-installed NOMEPACKAGE`, come con numpy nell'immagine qui sotto:

![Figura: Numpy-Issue2](img/Numpy-Issue1-Sol.png)

Il package indicato sarà quindi installato. A quel punto, riavviare il kernel (il motore) del foglio Jupyter. Ciò si può fare cliccando sul menù Kernel e sulla voce `Restart  & Clear Output`:

![Figura: RestartKernel](img/KernelRestartClearOutput.png)

Verificare che l'errore `no module named XXX` e altri correlati siano spariti.

2. Aprendo una nuova finestra di terminale, sempre con attivo l'environment ROexam, digitare il comando `pip install --ignore-installed NOMEPACKAGE`. Una volta conclusa l'installazione, tornare sul foglio Jupyter, andare sul menù Kernel e cliccare sulla voce `Restart  & Clear Output`.

__Nota__: può capitare che il nome del package non coincida completamente con il nome del modulo che dà errore (e.g., per usare il modulo yaml serve in realtà la libreria PyYaml ed è questo nome che dovrà essere in caso usato nel comando; controllare su Internet per accertarsene).

3. __Kernel shutdown__: se per qualche motivo si è chiusa la scheda del browser contenente il foglio Jupyter, si può provare a riaprirlo direttamente oppure a fare _shutdown_ del kernel ancora in esecuzione, andando sulla scheda `Running` e cliccando `Shutdown` del kernel relativo al foglio desiderato:

![Figura: KernelShutdown](img/Shutdown.png)

In seguito si può riaprire il foglio Jupyter e cliccare nuovamente su `Avvio esercizio` per ricaricare le celle necessarie e far sparire i codici.

4. __Jupyter Widget non visualizzati__: riaprendo il foglio dopo averlo chiuso, potrebbero non visualizzarsi i widget da usare per poter rispondere alle richieste dell'esercizio:

![Figura: NoJupyterWidget](img/JupyterWidget2.jpg)

Anche in questo caso, scegliendo nel menù Kernel la voce `Restart & Clear Output`, dovrebbe tornare a visualizzarsi la barra con le possibili modalità di risposta.

## C) Problemi con il salvataggio e l'esportazione del foglio in HTML

1. __Salva & Esporta__: cliccando sul bottone `Salva & Esporta` per creare la rendition in HTML del foglio Jupyter, su alcuni browser sembra che l'esecuzione della funzione sia errata, perché i messaggi di log appaiono su sfondo rosso, come nell'immagine seguente:

![Figura: SalvaEsportaOK](img/SalvaEsportaOK.jpg)

In realtà in questo caso è tutto a posto. I messaggi di log infatti si riferiscono alla conversione del foglio .ipynb in un .html, all'inserimento delle eventuali immagini presenti nel foglio e alla scrittura vera e propria del file .html nella sottocartella preview.

2. __Popup__: se non ci sono stati problemi, la funzione `Salva & Esporta` termina con l'apertura di una nuova scheda del browser per visualizzare il file .html appena creato. Alcuni browser potrebbero mostrare un avviso indicante il blocco delle finestre popup oppure il simbolo della finestra bloccata:

- Firefox e Chrome:
![Figura: PopupFirefox](img/PopupFirefox.jpg)

- Safari:
![Figura: PopupSafari](img/PopupSafari.png)

Per aprire il file .html, semplicemente cliccare sul messaggio di avviso e dare i consensi necessari oppure fare click sul simbolo della finestra bloccata:

![Figura: PopupSafari2](img/PopupSafari2.png)

3. __404 Not Found__: se qualcosa è andato storto nella creazione della rendition in .html, la finestra popup che si apre mostrerà l'errore seguente:

![Figura: PreviewNotFound](img/PreviewNotFound.jpg)

Controllate quindi il messaggio di errore che sarà indicato nel foglio Jupyter sotto il bottone `Salva & Esporta`. Potrebbe essere qualcosa del genere:

![Figura: ErroreHTML](img/NoJupyterContribExtensions.jpg)

In questo caso, procedere come nel problema 2 della sezione A: inserire una nuova cella codice e digitare `! pip install --ignore-installed jupyter-contrib-nbextensions && jupyter contrib nbextension install --user` per re-installare il package `jupyter-contrib-nbextensions`. Chiudere tutto (compreso il terminale) e riavviare Jupyter. Controllare che, nella home page del server Jupyter, sia presente la scheda `nb` con i seguenti check:
- contrib\_nb\_extensions\_help\_item
- Hide input
- Initialization cells
- ipysheet/extensions
- jupyter-js-widgets/extensions
- Nbextensions edit menu item
- Nbextensions dashboard tab

![Figura: JupyterNbExtensions](img/Jupyter-nbextensions.png)

Infine riprovare a esportare il foglio in .html.
