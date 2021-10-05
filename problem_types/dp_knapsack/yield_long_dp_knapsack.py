#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import re
from pprint import pprint
from tabulate import tabulate
from io import StringIO

INFO_UNIVERSE = {'instance_design','eval_support','feedback','explanations','resolving_code'}
    
CATEGORY='dp_knapsack'
def usage():
    print(f"""This script ({sys.argv[0]}) serves in the generation process of problems in the category '{CATEGORY}'. It mainly generates a full source yaml file problem starting from a tiny yaml file containing only the instance (specifically encoded as for problems of the '{CATEGORY}' category). The generated file can be used as the source for the later generation of the Jupyter notebooks or others formats in which the exercises or parts of them are actually rendered. Some of these formats are meant to support features like contextual assistance to the student (during the the exam or when training) or related activities like evaluation and grading work.

Right now, this script requires precisely one argument. The unique argument to this script should be the fullname of the .instance file containing an instance for problem {CATEGORY}. Right now this fullname is expected to have .instance as extension!

Right now the script writes down on stdout the extended yaml file including the additional authomatically generated fields offering the support information for the specific fields and for the field categories that have been required (support in the evaluation process, explanations or feedback to the students, instance design).

Usage example:
   ${sys.argv[0]} ../../collections/RO-2021-06-18/dp_knapsack/01/dp_knapsack.instance

The file ../../collections/RO-2021-06-18/dp_knapsack/01/dp_knapsack.instance is only rquired to contain the `instance` field with the instance defining data for problem category {CATEGORY}.

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
    elementi= instance['elementi']
    pesi= instance['pesi']
    valori= instance['valori']
    CapacityMax= instance['CapacityMax']
    task=source_instance_dict['tasks'][task_number-1][task_number]

    edrCapMax=[]
    edrCapGen=[]
    for tsk in range(1,1+len(source_instance_dict['tasks'])):
        if 'edrCapMax' in source_instance_dict['tasks'][tsk-1][tsk].keys():
            edrCapMax = source_instance_dict['tasks'][tsk-1][tsk]['edrCapMax']
        if 'edrCapGen' in source_instance_dict['tasks'][tsk-1][tsk].keys():
            edrCapGen = source_instance_dict['tasks'][tsk-1][tsk]['edrCapGen']
    items = [ [label, peso, val] for label, peso, val in  zip(elementi,pesi,valori) if label not in edrCapMax and label not in edrCapGen ] + [ [label, peso, val] for label, peso, val in  zip(elementi,pesi,valori) if label in edrCapMax and label not in edrCapGen ] + [ [label, peso, val] for label, peso, val in  zip(elementi,pesi,valori) if label in edrCapGen and label not in edrCapMax ] + [ [label, peso, val] for label, peso, val in  zip(elementi,pesi,valori) if label in edrCapMax and label in edrCapGen ]
    n = len(items)
    max_val_for_genCap = { i : [0]*(1+CapacityMax) for i in range(n+1) }
    for item, i in zip(items,range(1,1+n)):
      label, peso, val = item
      for b in range(1+CapacityMax):
          max_val_for_genCap[i][b] = max_val_for_genCap[i-1][b]
          if peso <= b:
              max_val_for_genCap[i][b] = max(max_val_for_genCap[i][b], val+max_val_for_genCap[i-1][b-peso])
    
    
    def reconstruct_opt(B : int, i : int):
        """restituisce opt_val ed opt_sol nell'ipotesi che siano disponibili solo i primi i elementi e B sia il budget (capacità dello zaino)"""
        promise = opt_val = max_val_for_genCap[i][B]
        basket = []
        while promise > 0:
            if max_val_for_genCap[i-1][B] < max_val_for_genCap[i][B]:
                basket.append(items[i-1])
                B -= items[i-1][1]
                assert B >= 0                
                promise -= items[i-1][2]
            i -= 1
        assert opt_val == sum(val for label, peso, val in basket)
        return opt_val, basket

    if task_codename == 'max-val_CapacityMax':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            max_val, opt_sol = reconstruct_opt(CapacityMax, n)
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_val}", file=fout)
        if 'explanations' in addenda:
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print("     Definiamo la matrice `max_val_for_genCap` che ha n+1 righe (la riga 1+i è labellata dall'inserimento di un i-esimo item nel set dei candidati tra cui pescare) e CapacityMax+1 colonne (labellate da un badget b con 0<=b<=CapacityMax) dove `max_val_for_genCap`[i,b] = massimo valore si un subset degli items 1 ... i  con somma dei pesi al più b.", file=fout)
            print("     Stampa della matrice `max_val_for_genCap`:", file=fout)
            #print(max_val_for_genCap)
            DP_table_as_dict_of_iterables = {'none': [0]*(1+CapacityMax) }
            for i in range(n):
                DP_table_as_dict_of_iterables["+ "+items[i][0]] = max_val_for_genCap[i+1]
            mybuffer=StringIO(tabulate(DP_table_as_dict_of_iterables, headers='keys', tablefmt='fancy_grid', showindex=range(1+CapacityMax)))
            for line in mybuffer.readlines():
                print("      "+line, file=fout)
        return

    if task_codename == 'opt-sol_CapacityMax':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            max_val, opt_sol = reconstruct_opt(CapacityMax, n)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {opt_sol}", file=fout)
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print("     Le informazioni che mi servono sono contenute nella matrice `max_val_for_genCap`.", file=fout)
        return

    if task_codename == 'max-val_CapacityMax_dopo-esclusioni':
        edrCapMax= task['edrCapMax']
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            max_val, opt_sol = reconstruct_opt(CapacityMax, n-len(edrCapMax))
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_val}", file=fout)
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print(f"     Avendo avuto l'attenzione di considerare per ultimi quegli elementi che in questo task mi si chiede di non considerare, l'informazione richiesta è `max_val_for_genCap`[i=new_n={n-len(edrCapMax)}][b=CapacityMax={CapacityMax}].", file=fout)
        return

    if task_codename == 'opt-sol_CapacityMax_dopo-esclusioni':
        edrCapMax= task['edrCapMax']
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            max_val, opt_sol = reconstruct_opt(CapacityMax, n-len(edrCapMax))
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {opt_sol}", file=fout)
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print(f"     Avendo avuto l'attenzione di considerare per ultimi quegli elementi che in questo task mi si chiede di non considerare, l'informazione richiesta è `max_val_for_genCap`[i=new_n={n-len(edrCapMax)}][b=CapacityMax={CapacityMax}].", file=fout)
        return

    if task_codename == 'max-val_CapacityGen':
        CapacityGen= task['CapacityGen']
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            max_val, opt_sol = reconstruct_opt(CapacityGen, n)
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_val}", file=fout)
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print(f"     L'informazione richiesta è `max_val_for_genCap`[n={n}][b=CapacityGen={CapacityGen}].", file=fout)
        return

    if task_codename == 'opt-sol_CapacityGen':
        CapacityGen= task['CapacityGen']
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            max_val, opt_sol = reconstruct_opt(CapacityGen, n)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {opt_sol}", file=fout)
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print("     Le informazioni che mi servono sono contenute nella matrice `max_val_for_genCap`.", file=fout)
        return

    if task_codename == 'max-val_CapacityGen_dopo-esclusioni':
        CapacityGen= task['CapacityGen']
        edrCapGen= task['edrCapGen']
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            max_val, opt_sol = reconstruct_opt(CapacityGen, n-len(edrCapGen))
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_val}", file=fout)
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print(f"     Avendo avuto l'attenzione di considerare per ultimi quegli elementi che in questo task mi si chiede di non considerare, l'informazione richiesta è `max_val_for_genCap`[i=new_n={n-len(edrCapGen)}][b=CapacityGen={CapacityGen}].", file=fout)
        return
        
    if task_codename == 'opt-sol_CapacityGen_dopo-esclusioni':
        CapacityGen= task['CapacityGen']
        edrCapGen= task['edrCapGen']
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            max_val, opt_sol = reconstruct_opt(CapacityGen, n-len(edrCapGen))
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {opt_sol}", file=fout)
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print(f"     Avendo avuto l'attenzione di considerare per ultimi quegli elementi che in questo task mi si chiede di non considerare, l'informazione richiesta è `max_val_for_genCap`[i=new_n={n-len(edrCapGen)}][b=CapacityGen={CapacityGen}].", file=fout)
        return

    print(f"ERROR: codename {task_codename} is an unknown codename for tasks!", file=sys.stderr)
    exit(1)


def put_standardized_items(tag, std_select, source_instance_dict, task_codename, task_number, fout):
    instance=source_instance_dict['instance']
    elementi= instance['elementi']
    pesi= instance['pesi']
    valori= instance['valori']
    CapacityMax= instance['CapacityMax']
    task=source_instance_dict['tasks'][task_number-1][task_number]
            
    if tag == "verif":
        if task_codename == 'max-val_CapacityMax':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_knapsack(elementi,pesi,valori,CapacityMax,answer{num_of_question}, pt_green=1, pt_red={task["tot_points"]}, index_pt={num_of_question-1}, val_or_sol="val")))'""", file=fout)
                return
        if task_codename == 'opt-sol_CapacityMax':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_knapsack(elementi,pesi,valori,CapacityMax,answer{num_of_question}, pt_green=1, pt_red={task["tot_points"]}, index_pt={num_of_question-1}, val_or_sol="sol")))'""", file=fout)
                return
        if task_codename == 'max-val_CapacityMax_dopo-esclusioni':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_knapsack(elementi,pesi,valori,CapacityMax,answer{num_of_question}, pt_green=1, pt_red={task["tot_points"]}, index_pt={num_of_question-1}, val_or_sol="val",edr={task["edrCapMax"]})))'""", file=fout)
                return
        if task_codename == 'opt-sol_CapacityMax_dopo-esclusioni':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_knapsack(elementi,pesi,valori,CapacityMax,answer{num_of_question}, pt_green=1, pt_red={task["tot_points"]}, index_pt={num_of_question-1}, val_or_sol="sol",edr={task["edrCapMax"]})))'""", file=fout)
                return
        if task_codename == 'max-val_CapacityGen':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_knapsack(elementi,pesi,valori,{task["CapacityGen"]},answer{num_of_question}, pt_green=1, pt_red={task["tot_points"]}, index_pt={num_of_question-1}, val_or_sol="val")))'""", file=fout)
                return
        if task_codename == 'opt-sol_CapacityGen':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_knapsack(elementi,pesi,valori,{task["CapacityGen"]},answer{num_of_question}, pt_green=1, pt_red={task["tot_points"]}, index_pt={num_of_question-1}, val_or_sol="sol")))'""", file=fout)
                return
        if task_codename == 'max-val_CapacityGen_dopo-esclusioni':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_knapsack(elementi,pesi,valori,{task["CapacityGen"]},answer{num_of_question}, pt_green=1, pt_red={task["tot_points"]}, index_pt={num_of_question-1}, val_or_sol="val",edr={task["edrCapGen"]})))'""", file=fout)
                return
        if task_codename == 'opt-sol_CapacityGen_dopo-esclusioni':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_knapsack(elementi,pesi,valori,{task["CapacityGen"]},answer{num_of_question}, pt_green=1, pt_red={task["tot_points"]}, index_pt={num_of_question-1}, val_or_sol="sol",edr={task["edrCapGen"]})))'""", file=fout)
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

