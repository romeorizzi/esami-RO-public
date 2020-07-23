#!/bin/bash

# set -x

FILE_PROFILO_ESERCIZI_PER_STUDENTE="profilo_esercizi_per_studente.csv"

if [ ! -e $FILE_PROFILO_ESERCIZI_PER_STUDENTE ]; then
    echo
    echo "   WARNING: Non trovo il file $FILE_PROFILO_ESERCIZI_PER_STUDENTE di cui necessito per lavorare. Esco subito dallo script."
    echo
    exit 1
fi

case $# in
     1)
	 echo "NUM_EXERCISE=$1"
         sort -t, -k $((3+$1)) profilo_esercizi_per_studente.csv
	 echo "NUM_EXERCISE=$1"
         ;;
      
     2)
	 NUM_MATCHING_LINES=$( cat $FILE_PROFILO_ESERCIZI_PER_STUDENTE | grep $2 - | wc -l | cut -f1 -d" ")
	 if [[ $NUM_MATCHING_LINES -gt 1 ]]
         then
             echo "More lines match your pattern:"
             NUM_COL_EXERCISE=$((3+$1))
             cat $FILE_PROFILO_ESERCIZI_PER_STUDENTE | sort -t, -k $NUM_COL_EXERCISE | grep -n --color=always $2 -
	 elif [[ $NUM_MATCHING_LINES -eq 0 ]]
         then
             echo "Sorry, no line matches your pattern! ($2)"
	 else
             NUM_COL_EXERCISE=$((3+$1))
             #echo "NUM_COL_EXERCISE=$NUM_COL_EXERCISE"
             NUM_LINES=$(wc -l $FILE_PROFILO_ESERCIZI_PER_STUDENTE | cut -f1 -d" ")
             #echo "NUM_LINES=$NUM_LINES"
             MATCH_LINE=$( cat $FILE_PROFILO_ESERCIZI_PER_STUDENTE | sort -t, -k $NUM_COL_EXERCISE | grep -n $2 - | cut -d: -f1 )
             echo "NUM_EXERCISE=$1 : MATCH_LINE=$MATCH_LINE/$NUM_LINES"
             COUNT=$(($NUM_LINES-$MATCH_LINE))
             #echo "COUNT=$COUNT"
             cat $FILE_PROFILO_ESERCIZI_PER_STUDENTE | sort -t, -k $NUM_COL_EXERCISE | tail -n $COUNT
             echo "NUM_EXERCISE=$1 : MATCH_LINE=$MATCH_LINE/$NUM_LINES"
         fi
         ;;
      
     *)
         echo
         echo "This script requires two arguments (but the second is optional):"
         echo "   numero dell'esercizio in base al quale vogliamo ordinare gli studenti nel file profilo_esercizi_per_studente.csv (per concentrare la nostra correzione su quel singolo esercizio)"
         echo "   matricola dello studente appena fatto (opzionale)"
         echo "First Example Usage: $0 3"
         echo "Second Example Usage: $0 3 VR4216"
         echo "Third Example Usage: $0 3 R421 | head"
         echo "Fourth Example Usage: $0 3 2163 | head -n 2"
         echo
         exit 1
esac

# set +x
