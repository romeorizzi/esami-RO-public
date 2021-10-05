#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import re
from pprint import pprint

INFO_UNIVERSE = {'instance_design','eval_support','feedback','explanations','resolving_code'}
    
CATEGORY='dp_triangle'
def usage():
    print(f"""This script ({sys.argv[0]}) serves in the generation process of problems in the category '{CATEGORY}'. It mainly generates a full source yaml file problem starting from a tiny yaml file containing only the instance (specifically encoded as for problems of the '{CATEGORY}' category). The generated file can be used as the source for the later generation of the Jupyter notebooks or others formats in which the exercises or parts of them are actually rendered. Some of these formats are meant to support features like contextual assistance to the student (during the the exam or when training) or related activities like evaluation and grading work.

Right now, this script requires precisely one argument. The unique argument to this script should be the fullname of the .instance file containing an instance for problem {CATEGORY}. Right now this fullname is expected to have .instance as extension!

Right now the script writes down on stdout the extended yaml file including the additional authomatically generated fields offering the support information for the specific fields and for the field categories that have been required (support in the evaluation process, explanations or feedback to the students, instance design).

Usage example:
   ${sys.argv[0]} ../../collections/RO-2021-06-18/dp_triangle/01/dp_triangle.instance

The file ../../collections/RO-2021-06-18/dp_triangle/01/dp_triangle.instance is only rquired to contain the `instance` field with the instance defining data for problem category {CATEGORY}.

Work in progress ... (see also other scripts to get the wider picture of what still needs to be implemented).

""")

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'

def explain_info_addenda_profile(turned_off_info):
    addenda = INFO_UNIVERSE - turned_off_info
    for item in addenda:
        print(f"Info element {item}: {CBOLD}{CGREEN}on{CEND}",file=sys.stderr)
    for item in turned_off_info:
        print(f"Info element {item}: {CBOLD}{CRED}OFF{CEND}",file=sys.stderr)
    print(file=sys.stderr)

def yield_info_addenda(source_instance_dict, task_codename, task_number, turned_off_info, fout):
    addenda = INFO_UNIVERSE - turned_off_info
    instance=source_instance_dict['instance']
    triangle= instance['triangle']
    task=source_instance_dict['tasks'][task_number-1][task_number]

    """ an hardcoded instance used for debugging and fast prototyping:
    triangle= [ [14,  0,  0,  0,  0, 0, 0],
                [12, 18,  0,  0,  0, 0, 0],
                [20, 13, 10,  0,  0, 0, 0],
                [19, 47, 35, 24,  0, 0, 0],
                [21, 52, 17, 44, 15, 0, 0],
                [50, 12, 20, 55, 52, 70, 0],
                [15, 12, 17, 13, 11, 15, 14]]
    """

    N=len(triangle)
    best_path_from = [ [ 0 ] * (1+N) for i in range(1+N) ]
    for i in range(N-1,-1,-1):
      for j in range(i+1):
          best_path_from[i][j] = triangle[i][j] + max(best_path_from[i+1][j],best_path_from[i+1][j+1])
    if task_codename == 'max_val_path':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {best_path_from[0][0]}", file=fout)
        if 'explanations' in addenda:
            print(f"\n    AUX__spiegazione: |", file=fout)
            print("     Embeddiamo il triangolo in una matrice triangolare inferiore e definiamo una seconda matrice triangolare `best_path_from` dove `best_path_from`[i,j] = massima somma dei valori su un cammino a scendere dalla posizione (i,j). Pertanto, `best_path_from`[0,0] contiene il valore desiderato e, al tempo stesso, è facile calcolare tutti questi valori salendo dal basso.", file=fout)
            print("\n     Stampa della matrice `best_path_from`:", file=fout)
            for i in range(1+N):
                for j in range(1+i):
                    print(f"      {best_path_from[i][j]:4}", end=" ", file=fout)
                print(file=fout)
            print("     Notate l'uso delle sentinelle: un'ultima riga di zeri ci ha consentito di applicare una semplice regola uniforme a tutti le celle.", file=fout)
        if 'resolving_code' in addenda:
            print(f"\n    AUX__codice_che_ha_prodotto_la_matrice_best_path_from: |", file=fout)
            print("""\
                N=len(triangle)
                best_path_from = [ [ 0 ] * (1+N) for i in range(1+N) ]
                for i in range(N-1,-1,-1):
                  for j in range(i+1):
                      best_path_from[i][j] = triangle[i][j] + max(best_path_from[i+1][j],best_path_from[i+1][j+1])
            """, file=fout)
        return
    elif task_codename == 'subproblems_family_and_recurrence':
        return
    elif task_codename == 'what_if_with_obliged_cell':
        return
    else:
        print(f"ERROR: codename {task_codename} is an unknown codename for tasks!", sys.stderr)
        exit(1)
   


def put_standardized_items(tag, std_select, source_instance_dict, task_codename, task_number, fout):
    instance=source_instance_dict['instance']
    triangle= instance['triangle']
    task=source_instance_dict['tasks'][task_number-1][task_number]
            
    if tag == "verif":
        if task_codename == '':
            if std_select == 'early_standard':
                print("""    verif: ''""", file=fout)
                return

        
    print(f"ERROR: '{std_select}' is an unknown standard for the tag '{tag}' in tasks of codename={task_codename}!", sys.stderr)
    exit(1)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Error: This script requires precisely one argument, you called it with {len(sys.argv)-1} arguments!\n")
        usage()
        exit(1)
    filename_in = sys.argv[1]
    if filename_in[-9:] != f".instance":
        print(f"Error: The unique argument to this script should be the fullname of the .instance file containing an instance for problem {CATEGORY}. This fullname is expected to have .instance as extension!\n")
        usage()
        exit(1)
    if not os.path.exists(filename_in):
        print(f"\nError: I could not find the file:\n    {filename_in}\nScript aborting.")
        exit(1)
    with open(filename_in) as file:
        try:
            source_instance_dict = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            print(f"Attenzione! Il file yaml ({filename_in}) appare CORROTTO")
            exit(1)

    turned_off_info = set({})
    #pprint(source_instance_dict['instance'], indent=1, width=160, depth=None, compact=True)
    explain_info_addenda_profile(turned_off_info)
    print("tasks:")
    for tsk in range(1,1+len(source_instance_dict['tasks'])):
        print(f"- {tsk}:")
        yield_info_addenda(source_instance_dict, source_instance_dict['tasks'][tsk-1][tsk]['task_codename'], tsk, turned_off_info, fout=sys.stdout)
    exit(0)

