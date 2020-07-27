# -*- coding: utf-8 -*-
"""
@authors: Adriano Tumminelli
"""

import hashlib
import zipfile
import os
import os.path


def sha1_file(filename):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data) 
 
    return sha1.hexdigest()


map_save_path = "map_export.txt"

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def handler_save_map(params): 
    
    if not "data" in params:
        return "error"

    data = params["data"][0]
    
    with open(map_save_path, "w") as f:
        f.write(data)
        
    # generare nome della cartella dove collocare la consegna
    if os.path.exists('../consegna_esameRO-2020-07-27'):
        return "directory_error la cartella consegna_esameRO-2020-07-27 esiste già. Se vuoi procedere con nuova consegna rimuovila o spostala altrove."
    os.mkdir("../consegna_esameRO-2020-07-27")
    fname_base = os.path.basename(os.getcwd()) + ".zip"
    fname = "../consegna_esameRO-2020-07-27/" + fname_base
    print(fname)
    zipf = zipfile.ZipFile(fname, 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
    
    sha1_str = sha1_file(fname)
    with open("../consegna_esameRO-2020-07-27/firma_anticipata.txt", "w") as f:
        f.write(
"""
Invia la seguente firma digitale del file '{filename}'  

{sha1}

al Gruppo Telegram del Corso:
    https://t.me/RicercaOperativa2020

se non ti è pratico allora puoi mandare una mail a ENTRAMBI i seguenti indirizzi:
    romeo.rizzi@univr.it
    alice.raffaele@univr.it

Se non hai o perdi la connessione internet puoi inviare la firma digitale tramite SMS al seguente numero:
cel:+39.3518684000


ATTENZIONE: Non apportare modifiche allo zip altrimenti la firma digitale del file non corrisponderà piu' a quella calcolata.
(E non potremo accettarlo se non ci perviene esso stesso entro i tempi concordati per la consegna nonostante le sue grosse dimensioni.)
""".format(
    filename = fname_base,
    sha1 = sha1_str
)
        )

    return "done Archivio dell'esame generato correttamente (lo trovi nella cartella 'consegna_esameRO-2020-07-27', sorella del folder entro il quale hai svolto il tuo esame. Se vuoi riprodurre una nuova consegna devi prima rimuovere o spostare questa cartella.)\n\nProcedi subito alla tua sottomissione e chiusura dell'esame (istruzion nel file 'firma_anticipata.txt' che trovi nella cartella consegna)"

def handler_test(params):
    return "ciao " + str(params)

handlers = {
    "save" : handler_save_map,
    "test": handler_test
}

def handle_message(params):
    cmd_type = params['type'][0]
    if cmd_type in handlers:
        return handlers[cmd_type](params)
    return "error"
    
    
