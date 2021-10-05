#!/usr/bin/python3
from sys import argv, exit, stderr
import os
import random
import string
import re

INPUT_FILE = "lista_studenti_iscritti_tmpversion.csv"
OUTPUT_FILE = "lista_studenti_iscritti_con_chiavi.csv"

def usage():
    print(f"""Usage: ./{os.path.basename(argv[0])} [-h] [-n] [length_pwd (int, default = 6) [PWD_PREFIX (string, "") [PWD_SUFFIX (string, "") [lenght_anchor (int, -1)] ] ] ]\n\n   dove un flag che inizi per h condurrebbe a visualizzare questo aiuto ed il flag n chiede che la password generata sia un codice numerico\n\n   il primo parametro opzionale (length_pwd) è un numero intero che indica la lunghezza della sezione randomica della password di accesso (default 6, può essere 0 se non vogliamo alcuna password).\n\n   il secondo parametro opzionale (PWD_PREFIX) e' un'eventuale stringa di prefisso uguale per tutte le password (default la stringa vuota).\n     Nota: alcuni valori particolari di PWD_PREFIX vengono serviti in modo speciale, si veda il codice.\n\n   il terzo parametro opzionale (PWD_SUFFIX) e' un'eventuale stringa di suffisso uguale per tutte le password (default la stringa vuota).\n     Nota: alcuni valori particolari di PWD_SUFFIX possono essere gestiti in modo speciale.\n\n   il quarto parametro opzionale (lenght_anchor) è la lunghezza dell'ancora nell'indirizzo a cui lo studente reperisce i propri file col tema assegnato (consigliato 10, possibile 0 che implica che tutte le ancore siano la stringa vuota, ma il default è -1 nel qual caso il file .csv generato non conterrà la colonna per le ancore generate randomicamente e specifiche al singolo studente).\n\nEsempi d'uso:\n   Nel caso dell'esame di Ricerca Operativa in UniVR lo lancio come:\n   ./{os.path.basename(argv[0])} -n 6 "" "" 15\n   Nel caso dell'esame di Algoritmi in UniVR se l'esame sarà in telematico lo lancio come:\n   ./{os.path.basename(argv[0])}  8 "" "" -1""", file=stderr)
    exit(1)

# THE MAIN PROGRAM:    
# Usage: command_name  [-h] [-n] [length_pwd (int, default = 6) [PWD_PREFIX (string, "") [PWD_SUFFIX (string, "") [lenght_anchor (int, -1)] ] ] ]
if len(argv) > 1 and argv[1][:2] == "-h":
    print("Serviamo la tua RICHIESTA DI AIUTO:", file=stderr)
    usage()
    exit(1)

numeric_pwd = 0    
if len(argv) > 1 and argv[1][:2] == "-n":
    numeric_pwd = 1

if len(argv)-numeric_pwd > 5:
    print("ERROR: Hai fornito troppi parametri (più di 4)!", file=stderr)
    usage()
    exit(1)

if len(argv)-numeric_pwd > 1:
  try:
    length_pwd = int(argv[1+numeric_pwd])
  except ValueError:
    print(f"ERROR: The first optional argument is present but it is not an int (ha valore {argv[1+numeric_pwd]})!", file=stderr)
    usage()
else:
    length_pwd = 6

if len(argv)-numeric_pwd > 4:
  try:
    length_anchor = int(argv[4+numeric_pwd])
  except ValueError:
    print(f"ERROR: The fourth optional argument is present but it is not an int (ha valore {argv[4+numeric_pwd]})!", file=stderr)
    usage()
else:
    length_anchor = -1

PWD_PREFIX = PWD_SUFFIX = ""
if len(argv)-numeric_pwd > 2:
    PWD_PREFIX = argv[2+numeric_pwd]
if len(argv)-numeric_pwd > 3:
    PWD_SUFFIX = argv[3+numeric_pwd]

def PWD_prefix(MATRICOLA,SURNAME,NAME,YEAR,ID_STUDENT):
    if PWD_PREFIX == "MATRICOLA":
        return MATRICOLA
    elif PWD_PREFIX == "NAME":
        return re.sub('[ ]', '', NAME)
    elif PWD_PREFIX == "SURNAME":
        return re.sub('[ ]', '', SURNAME)
    else:
        return PWD_PREFIX  

def PWD_suffix(MATRICOLA,SURNAME,NAME,YEAR,ID_STUDENT):
    if PWD_SUFFIX == "MATRICOLA":
        return MATRICOLA
    elif PWD_SUFFIX == "NAME":
        return re.sub('[ ]', '', NAME)
    elif PWD_SUFFIX == "SURNAME":
        return re.sub('[ ]', '', SURNAME)
    else:
        return PWD_SUFFIX  

        
if not os.path.exists(INPUT_FILE):
    print(f"Questo script ({argv[0]}) opera a partire dal file {INPUT_FILE} che assume esistere nella sua stessa cartella.\nESECUZIONE INTERROTTA: File non trovato.", file=stderr)
    exit(1)

if os.path.exists(OUTPUT_FILE):
    print(f"Questo script ({argv[0]}) genera un file di nome {OUTPUT_FILE} nella sua stessa cartella.\nESECUZIONE INTERROTTA: File esiste già. Cancellalo o spostalo prima di richiederne una nuova generazione.", file=stderr)
    exit(1)
    

# Esempio di utilizzo di tabella di conversione:
#intab = "$"
#outtab = " "
# Ma per ora non sono emerse situazioni dove sia stato necessario disinfettare dei caratteri e quindi, teniamo presente lo strumento (un filtro di depurazione), ma lasciamolo girare a vuoto:
intab = ""
outtab = ""
trantab = str.maketrans(intab, outtab)    

fout = open(OUTPUT_FILE,"w")
with open(INPUT_FILE,"r") as fin:
    i = 0
    for line in list(fin) + ['"VR123456","TEST","MY","2001/2002","id123456@studenti.univr.it"']:  # AGGIUNTA UN'ULTIMA UTENZA PER IL TESTING:
       i+=1 
       MATRICOLA, SURNAME, NAME, YEAR, MAILADR_ID = line.strip().split(',')
       MATRICOLA = re.sub('["]', '', MATRICOLA).translate(trantab)
       SURNAME = re.sub('["]', '', SURNAME).translate(trantab)
       NAME = re.sub('["]', '', NAME).translate(trantab)
       YEAR = re.sub('["]', '', YEAR).translate(trantab)
       MAILADR_ID = re.sub('["]', '', MAILADR_ID).translate(trantab)
       ID_STUDENT=MAILADR_ID[0:8]
       if ID_STUDENT=="id123456":
           MAIL_ADR = "romeo.rizzi@univr.it"
       else:
           MAIL_ADR = MAILADR_ID           
       #print(f"MATRICOLA={MATRICOLA}, YEAR={YEAR}, ID_STUDENT={ID_STUDENT}, NAME={NAME}, SURNAME={SURNAME}, MAIL_ADR={MAIL_ADR}")
       palette = string.ascii_letters + string.digits
       if numeric_pwd == 1:
           palette = string.digits
       PASSWORD = PWD_prefix(MATRICOLA,SURNAME,NAME,YEAR,ID_STUDENT) + \
                  ''.join([random.choice(palette) for n in range(length_pwd)]) + \
                  PWD_suffix(MATRICOLA,SURNAME,NAME,YEAR,ID_STUDENT)
       # USERNAME = MATRICOLA
       if length_anchor < 0:
           fout.write(MATRICOLA + "," + YEAR + "," + PASSWORD + "," + ID_STUDENT + "," + NAME + "," + SURNAME + "," + MAIL_ADR + "\n")
       else:
           ANCHOR = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length_anchor)])
           fout.write(MATRICOLA + "," + YEAR + "," + ANCHOR + "," + PASSWORD + "," + ID_STUDENT + "," + NAME + "," + SURNAME + "," + MAIL_ADR + "\n")
           
           
print(f"Fatto! Il file {OUTPUT_FILE} è stato costruito e contiene {i} records (l'ultimo è lo studente fake MY TEST).")
print(f"Per lo studente fake MY TEST, le mail saranno indirizzate all'indirizzo {MAIL_ADR} del docente.")

""" LEGENDA DEL RECORD DROPPATO SU FILE lista_studenti_iscritti_con_chiavi.csv:

Il singolo record (riga, dato studente) viene droppato sul file .csv in formazione col comando:

fout.write(MATRICOLA + "," + YEAR + "," + ANCHOR + "," + PASSWORD + "," + ID_STUDENT + "," + NAME + "," + SURNAME + "," + MAIL_ADR + "\n")

dove:

MATRICOLA è la matricola, che a UniVR è nella forma VR??????
YEAR è l'anno accademico in cui spettava (e tipicamente è avvenuta) la frequenza al corso
ANCHOR è una stringa di 15 caratteri (lettere maiuscole e minuscole + cifre) generata casualmente. La uso ad esempio per il nome della cartella da cui potranno fare il download del loro compito, ma possiamo usalra anche per altri usi. Nel generarla non ho utilizzato alcuna informazione specifica (come la matricola oppure la data dell'appello). Inoltre: non è intesa per essere riproducibie (lo script che genera il file vorrà essere di pubblico dominio).
PASSWORD: un codice numerico di 6 cifre
ID_STUDENT: è l'id studente (a volte all'esame ti arrivano con delle tessere su cui è scritto solo quello, inoltre questo id mantiene validità quando passano dalla triennale alla magistrale mentre la matricola cambia). Il formato dell'id studente a UniVR è id???xxx dove ??? sono 3 cifre e xxx o sono o tutte e tre cifre o tutte e tre lettere minuscole.
NAME è il nome dello studente
SURNAME è il cognome dello studente
MAIL_ADR è l'indirizzo mail dello studente 
"""

