# -*- coding: utf-8 -*-
"""
@authors: Adriano Tumminelli
"""

import hashlib
import zipfile
import os


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
        
    #dirname = ottenere nome cartella
    fname_base = os.path.basename(os.getcwd()) + ".zip"
    fname = "../" + fname_base
    print(fname)
    zipf = zipfile.ZipFile(fname, 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
    
    sha1_str = sha1_file(fname)
    with open("../firma_anticipata.txt", "w") as f:
        f.write(
"""
Invia la seguente firma digitale del file '{filename}'  

{sha1}

al Gruppo Telegram del Corso:
    https://t.me/RicercaOperativa2020

se non ti è pratico allora puoi mandare una mail a ENTRAMBI i seguenti indirizzi:
    romeo.rizzi@univr.it
    alice.raffaele@univr.it

Nel caso non avessi una connessione internet puoi inviare la firma digitale tramite SMS
al seguente numero:
cel:+39.3518684000


ATTENZIONE: Non apportare modifiche allo zip altrimenti la firma digitale del file non corrisponderà piu' a quella calcolata.
E non potremo accettarlo (a meno che lo zip non venga inviato subito nonostante le sue grosse dimensioni)
""".format(
    filename = fname_base,
    sha1 = sha1_str
)
        )

    return "done"

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
    
    