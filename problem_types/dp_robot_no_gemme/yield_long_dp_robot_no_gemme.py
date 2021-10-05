#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import re
from pprint import pprint

INFO_UNIVERSE = {'instance_design','eval_support','feedback','explanations','resolving_code'}
    
CATEGORY='dp_robot_no_gemme'
def usage():
    print(f"""This script ({sys.argv[0]}) serves in the generation process of problems in the category '{CATEGORY}'. It mainly generates a full source yaml file problem starting from a tiny yaml file containing only the instance (specifically encoded as for problems of the '{CATEGORY}' category). The generated file can be used as the source for the later generation of the Jupyter notebooks or others formats in which the exercises or parts of them are actually rendered. Some of these formats are meant to support features like contextual assistance to the student (during the the exam or when training) or related activities like evaluation and grading work.

Right now, this script requires precisely one argument. The unique argument to this script should be the fullname of the .instance file containing an instance for problem {CATEGORY}. Right now this fullname is expected to have .instance as extension!

Right now the script writes down on stdout the extended yaml file including the additional authomatically generated fields offering the support information for the specific fields and for the field categories that have been required (support in the evaluation process, explanations or feedback to the students, instance design).

Usage example:
   ${sys.argv[0]} ../../collections/RO-2021-06-18/dp_robot_no_gemme/01/dp_robot_no_gemme.instance

The file ../../collections/RO-2021-06-18/dp_robot_no_gemme/01/dp_robot_no_gemme.instance is only rquired to contain the `instance` field with the instance defining data for problem category {CATEGORY}.

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
    #pprint(instance, indent=1, width=160, depth=None, compact=True)
    campo_minato= instance['campo_minato']
    task=source_instance_dict['tasks'][task_number-1][task_number]

    """ an hardcoded instance used for debugging and fast prototyping:
    campo_minato=[
        [ " " , " " , " " , " " , " " , " " , " " , "*" , "*" ],
        [ " " , " " , " " , "*" , " " , "*" , " " , " " , " " ],
        [ " " , " " , " " , "*" , " " , " " , " " , " " , " " ],
        [ " " , " " , " " , " " , " " , " " , " " , "*" , " " ],
        [ " " , " " , "*" , " " , "*" , " " , " " , " " , " " ],
        [ " " , " " , " " , " " , " " , " " , "*" , " " , " " ],
        [ "*" , " " , "*" , " " , "*" , " " , " " , " " , " " ],
        [ " " , " " , " " , " " , " " , " " , " " , " " , " " ]
    ]
    start_point= "(2,5)"
    target_point= "(6,6)"
    middle_point= "(4,5)"
    """

    m = len(campo_minato)
    n = len(campo_minato[0])
    def read_str_as_pair_of_ints(pair_str):
        x,y=pair_str[1:-1].split(',')
        return (int(x),int(y))

    num_paths_to = [ [ 0 ] * (n+1) for i in range(m+1) ]
    num_paths_to[1][1] = 1
    for i in range(1,m+1):
      for j in range(1,n+1):
        if (i,j) != (1,1):
            num_paths_to[i][j] = 0 if campo_minato[i-1][j-1]=="*" else \
                num_paths_to[i-1][j]+num_paths_to[i][j-1]
    if task_codename == 'compute_num_paths_to':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    AUX__la_matrice_num_paths_to: |", file=fout)
            print("     Stampa della matrice `num_paths_to` (e righe e le colonne sono indicizzate partendo da 0, dove la prima riga e colonna vengono utili come sentinelle):", file=fout)
            print("          -",end=" ", file=fout)
            for j in range(1,n+1):
                print(f"{j:3}", end=" ", file=fout)
            print(file=fout)
            for i in range(m+1):
                print("      ",end="", file=fout)
                print(i if i>0 else '-', end=" ", file=fout)
                for j in range(n+1):
                    print(f"{num_paths_to[i][j]:3}", end=" ", file=fout)
                print(file=fout)

        if 'resolving_code' in addenda:
            print(f"\n    AUX__codice_che_ha_prodotto_la_matrice_num_paths_to: |", file=fout)
            print("""\
                 num_paths_to = [ [ 0 ] * (n+1) for i in range(m+1) ]
                 num_paths_to[1][1] = 1
                 for i in range(1,m+1):
                 for j in range(1,n+1):
                  if (i,j) != (1,1):
                    num_paths_to[i][j] = 0 if campo_minato[i-1][j-1]=="*" else num_paths_to[i-1][j]+num_paths_to[i][j-1]
            """, file=fout)

        return
    num_paths_from = num_paths_from = [ [ 0 ] * (n+2) for i in range(m+2) ]
    num_paths_from[m][n] = 1
    for i in range(m,0,-1):
      for j in range(n,0,-1):
        if (i,j) != (m,n):
            num_paths_from[i][j] = 0 if campo_minato[i-1][j-1]=="*" else \
                num_paths_from[i+1][j]+num_paths_from[i][j+1]
    if task_codename == 'compute_num_paths_from':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    AUX__la_matrice_num_paths_from: |", file=fout)
            print("     Stampa della matrice `num_paths_from` (e righe e le colonne sono indicizzate partendo da 0, dove l'ultima riga e colonna vengono utili come sentinelle):", file=fout)
            print("          -",end=" ", file=fout)
            for j in range(1,n+2):
                print(f"{j:3}", end=" ", file=fout)
            print(file=fout)
            for i in range(m+2):
                print("      ",end="", file=fout)
                print(i if i>0 else '-', end=" ", file=fout)
                for j in range(n+2):
                    print(f"{num_paths_from[i][j]:3}", end=" ", file=fout)
                print(file=fout)
        
        if 'resolving_code' in addenda:
            print(f"\n    AUX__codice_che_ha_prodotto_la_matrice_num_paths_from: |", file=fout)
            print("""\
                 num_paths_from = [ [ 0 ] * (n+2) for i in range(m+2) ]
                 num_paths_from[m][n] = 1
                 for i in range(m,0,-1):
                   for j in range(n,0,-1):
                     if (i,j) != (m,n):
                         num_paths_from[i][j] = 0 if campo_minato[i-1][j-1]=="*" else num_paths_from[i+1][j]+num_paths_from[i][j+1]
            """, file=fout)
        return

    assert(num_paths_to[m][n]==num_paths_from[1][1])
    if task_codename == 'num_paths_start_to_end':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_la_risposta_corretta: {num_paths_to[m][n]}  (ossia um_paths_to[{m}][{n}])", file=fout)
    elif task_codename == 'num_paths_cell_to_end':
        start_point= task['start_point']
        start_point=read_str_as_pair_of_ints(start_point)
        print(f"start_point[0]={start_point[0]}\nstart_point[1]={start_point[1]}")
        assert campo_minato[start_point[0] -1][start_point[1] -1] == " "
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_la_risposta_corretta: {num_paths_from[start_point[0]][start_point[1]]}  (ossia num_paths_from[{start_point[0]}][{start_point[1]}])", file=fout)
    elif task_codename == 'num_paths_start_to_cell':
        target_point= task['target_point']
        target_point=read_str_as_pair_of_ints(target_point)
        print(f"target_point[0]={target_point[0]}\ntarget_point[1]={target_point[1]}")
        assert campo_minato[target_point[0] -1][target_point[1] -1] == " "
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_la_risposta_corretta: {num_paths_to[target_point[0]][target_point[1]]}  (ossia num_paths_to[{target_point[0]}][{target_point[1]}])", file=fout)              
    elif task_codename == 'num_paths_through_cell':
        middle_point= task['middle_point']
        middle_point=read_str_as_pair_of_ints(middle_point)
        print(f"middle_point[0]={middle_point[0]}\nmiddle_point[1]={middle_point[1]}")
        assert campo_minato[middle_point[0] -1][middle_point[1] -1] == " "
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_la_risposta_corretta: {num_paths_to[middle_point[0]][middle_point[1]]*num_paths_from[middle_point[0]][middle_point[1]]}  (ossia num_paths_to[{middle_point[0]}][{middle_point[1]}]*num_paths_from[{middle_point[0]}][{middle_point[1]}])", file=fout)
    else:
        print(f"ERROR: codename {task_codename} is an unknown codename for tasks!", sys.stderr)
        exit(1)


def put_standardized_items(tag, std_select, source_instance_dict, task_codename, task_number, fout):
    instance=source_instance_dict['instance']
    campo_minato= instance['campo_minato']
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

