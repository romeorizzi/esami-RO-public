#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

COLLECTION_FOLDER = 'collections/'

def check_active_conda_env(required_conda_env):
    if not 'CONDA_DEFAULT_ENV' in os.environ:
        print(f"Sembra che nessun conda environment sia attualmente attivo. Tipicamente questo script ({sys.argv[0]}) richiede invece un environmnt (quale {required_conda_env}, da attivare prima con 'conda activate {required_conda_env}')")
        print("Sicuro di voler continuare? (sSyY per proseguire comunque)")
        risp=input()
        if risp.upper() not in {'s','S','Y'}:
            print(f"Ok, allora prima di chiamarmi attiva l'environment con:\n   conda activate {required_conda_env}")
            exit(0)
    elif os.environ['CONDA_DEFAULT_ENV'] != required_conda_env:
        print(f"Il tuo attuale conda environment è {os.environ['CONDA_DEFAULT_ENV']} invece che quello attualmente richiesto di default da questo script ({required_conda_env})")
        print("Sicuro di voler continuare? (sSyY per proseguire comunque)")
        risp=input()
        if risp.upper() not in {'s','S','Y'}:
            print(f"Ok, allora prima di chiamarmi attiva il corretto environment con:\n   conda activate {required_conda_env}")
            exit(0)

