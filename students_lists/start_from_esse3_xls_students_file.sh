#!/bin/bash
set -e
echo
echo "Sono lo script che crea automaticamente, secondo configurazioni standard per l'esame di Ricerca Operativa, i seguenti file:"
echo "   1. lista_studenti_iscritti.csv"
echo "   2. lista_studenti_iscritti_con_chiavi.csv"
echo " partendo dal file ListaStudentiEsameExport.xls degli studenti iscritti all'appello scaricato da Esse3."
echo
echo Usage: $0 [DATA_APPELLO]
echo " spiegazione: se il parametro opzionale DATA_APPELLO non è fornito, allora il file ListaStudentiEsameExport.xls viene cercato nella cartella corrente, altrimenti viene cercato nella cartella DATA_APPELLO"
echo " anche i file prodotti vengono generati nella cartella DATA_APPELLO oppure in quella corrente se DATA_APPELLO non è specificata"
echo
echo "ATTENZIONE: ricordati di non modificare questi file dopo che hai cominciato ad utilizzarli per non creare inconsistenze tra le varie cose che generi partendo da essi. Se li modifichi, riparti da capo, dall'esecuzione del presente script."
echo
if [ "$#" -gt 1 ]; then
    exit 1
fi
STARTDIR=$(pwd)
RELPATH=""
if [ "$#" -gt 0 ]; then
    RELPATH="$1/"
fi
echo "Creating the file: ${RELPATH}lista_studenti_iscritti_tmpversion.csv"
xls2csv ${RELPATH}ListaStudentiEsameExport.xls | cut -d, -f3,4,5,6,13 | sort | grep "^\"VR" > ${RELPATH}lista_studenti_iscritti_tmpversion.csv
echo "Done! A first temporary copy of the file ${RELPATH}lista_studenti_iscritti.csv has been created."
echo
echo "Creating the file: ${RELPATH}lista_studenti_iscritti_con_chiavi.csv"
if [ "$#" -ne 0 ]; then
    cd $RELPATH
    ../add_chiavi_al_csv_file.py -n 6 "" "" 15
    cd $STARTDIR
else
    ./add_chiavi_al_csv_file.py -n 6 "" "" 15
fi
echo "Fatto! The file ${RELPATH}lista_studenti_iscritti_con_chiavi.csv has been created."
cut -d, -f1,2,5,6,7 ${RELPATH}lista_studenti_iscritti_con_chiavi.csv > ${RELPATH}lista_studenti_iscritti.csv
echo "Fatto! The file ${RELPATH}lista_studenti_iscritti.csv has been created."
echo "Removing the file: ${RELPATH}lista_studenti_iscritti_tmpversion.csv"
rm ${RELPATH}lista_studenti_iscritti_tmpversion.csv
echo
