#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import re
from pprint import pprint

INFO_UNIVERSE = {'instance_design','eval_support','feedback','explanations','resolving_code'}
    
CATEGORY='dp_lcs'
def usage():
    print(f"""This script ({sys.argv[0]}) serves in the generation process of problems in the category '{CATEGORY}'. It mainly generates a full source yaml file problem starting from a tiny yaml file containing only the instance (specifically encoded as for problems of the '{CATEGORY}' category). The generated file can be used as the source for the later generation of the Jupyter notebooks or others formats in which the exercises or parts of them are actually rendered. Some of these formats are meant to support features like contextual assistance to the student (during the the exam or when training) or related activities like evaluation and grading work.

Right now, this script requires precisely one argument. The unique argument to this script should be the fullname of the .instance file containing an instance for problem {CATEGORY}. Right now this fullname is expected to have .instance as extension!

Right now the script writes down on stdout the extended yaml file including the additional authomatically generated fields offering the support information for the specific fields and for the field categories that have been required (support in the evaluation process, explanations or feedback to the students, instance design).

Usage example:
   ${sys.argv[0]} ../../collections/RO-2021-06-18/dp_lcs/01/dp_lcs.instance

The file ../../collections/RO-2021-06-18/dp_lcs/01/dp_lcs.instance is only rquired to contain the `instance` field with the instance defining data for problem category {CATEGORY}.

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
    s= instance['s']
    t= instance['t']
    task=source_instance_dict['tasks'][task_number-1][task_number]

    pref_of_len = [ [ 0 ] * (1+len(t)) for i in range(1+len(s)) ]
    for i in range(1,1+len(s)):
      for j in range(1,1+len(t)):
          if s[i-1] == t[j-1]:
              pref_of_len[i][j] = 1 + pref_of_len[i-1][j-1]
          else:
              pref_of_len[i][j] = max(pref_of_len[i-1][j],pref_of_len[i][j-1])

    suff_from_pos = [ [ 0 ] * (1+len(t)) for i in range((1+len(s))) ]
    for i in range(len(s)-1,-1,-1):
      for j in range(len(t)-1,-1,-1):
          if s[i] == t[j]:
              suff_from_pos[i][j] = 1 + suff_from_pos[i+1][j+1]
          else:
              suff_from_pos[i][j] = max(suff_from_pos[i+1][j],suff_from_pos[i][j+1])
    assert(pref_of_len[len(s)][len(t)]==suff_from_pos[0][0])
    
    def reconstruct_opt_lcs_pref_of_len(len_s,len_t, lcs : list):
        if pref_of_len[len_s][len_t] == 0:
            pass
        elif s[len_s-1] == t[len_t-1]:
            lcs.append(s[len_s-1])
            reconstruct_opt_lcs_pref_of_len(len_s-1,len_t-1, lcs)
        elif len_s==1:
            reconstruct_opt_lcs_pref_of_len(len_s,len_t-1, lcs)
        elif pref_of_len[len_s-1][len_t]==pref_of_len[len_s][len_t]:
            reconstruct_opt_lcs_pref_of_len(len_s-1,len_t, lcs)
        else:
            reconstruct_opt_lcs_pref_of_len(len_s,len_t-1, lcs)

    def reconstruct_opt_lcs_suff_from_pos(i,j, lcs : list):
        if suff_from_pos[i][j] == 0:
            pass
        elif s[i] == t[j]:
            lcs.append(s[i])
            reconstruct_opt_lcs_suff_from_pos(i+1,j+1, lcs)
        elif i==len(s)-1:
            reconstruct_opt_lcs_suff_from_pos(i,j+1, lcs)
        elif suff_from_pos[i+1][j]==suff_from_pos[i][j]:
            reconstruct_opt_lcs_suff_from_pos(i+1,j, lcs)
        else:
            reconstruct_opt_lcs_suff_from_pos(i,j+1, lcs)
            

    if task_codename == 'opt_lcs_s_t':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {pref_of_len[len(s)][len(t)]}", file=fout)

            lcs = []
            reconstruct_opt_lcs_pref_of_len(len(s),len(t), lcs)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {list(reversed(lcs))}", file=fout)

        if 'explanations' in addenda:
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print("     Definiamo la matrice `pref_of_len` che ha |s|+1 righe (labellate coi caratteri di s) e |t|+1 colonne (labellate coi caratteri di t)  dove `pref_of_len`[i,j] = massima lunghezza di una sottosequenza comune tra il prefisso s_i di s di lunghezza i e il suffisso t_j di t di lunghezza j. Le righe e le colonne sono indicizzate partendo da 0.", file=fout)
            print("     Stampa della matrice `pref_of_len`:", file=fout)
            print("         -",end="  ", file=fout)
            for j in range(len(t)):
                print(t[j], end="  ", file=fout)
            print(file=fout)
            for i in range(1+len(s)):
                print("      ", end="", file=fout)
                print(s[i-1] if i>0 else '-', end=" ", file=fout)
                for j in range(1+len(t)):
                    print(f"{pref_of_len[i][j]:2}", end=" ", file=fout)
                print(file=fout)

            print(f"     La matrice di cui sopra, consultata nella sua ultima cella, già consente di determinare la massima lunghezza  di una sottosequenza comune tra s e t ({pref_of_len[len(s)][len(t)]}) ed anche di ricostruire una tale soluzione ottima. Tale matrice, opportunamente consultata, consente di dare risposta anche ad altri quesiti, ma per affrontarne anche altri conviene dotarsi di una seconda matrice che, in modo simmetrico alla prima, consenta di risolvere la stessa domanda e riottenere lo stesso numero ({pref_of_len[len(s)][len(t)]}) da un'altra prospettiva.", file=fout)
            print("     Definiamo la matrice `suff_from_pos` che ha |s|+1 righe (labellate coi caratteri di s, l'ultima labellata con '-') e |t|+1 colonne (labellate coi caratteri di t, l'ultima labellata con '-')  dove `suff_from_pos`[i,j] = massima lunghezza di una sottosequnza comune tra il suffisso s^i di s che inizia col carattere i di s e il suffisso t^j di t che inizia col carattere j di t.", file=fout)          
            print("     Stampa della matrice `suff_from_pos`:", file=fout)
            print("         ", end="", file=fout)
            for j in range(len(t)):
                print(t[j], end="  ", file=fout)
            print("-", file=fout)
            for i in range(1+len(s)):
                print("      ", end="", file=fout)
                print(s[i] if i<len(s) else '-', end=" ", file=fout)
                for j in range(1+len(t)):
                    print(f"{suff_from_pos[i][j]:2}", end=" ", file=fout)
                print(file=fout)
        return
            
    if task_codename == 'opt_lcs_s_prefix':
        len_s_prefix= task["len_s_prefix"]            
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {pref_of_len[len_s_prefix][len(t)]}", file=fout)

            lcs = []
            reconstruct_opt_lcs_pref_of_len(len_s_prefix,len(t), lcs)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {list(reversed(lcs))}", file=fout)
        return
    
    if task_codename == 'opt_lcs_t_prefix':
        len_t_prefix= task["len_t_prefix"]            
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {pref_of_len[len(s)][len_t_prefix]}", file=fout)

            lcs = []
            reconstruct_opt_lcs_pref_of_len(len(s),len_t_prefix, lcs)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {list(reversed(lcs))}", file=fout)
        return

              
    if task_codename == 'opt_lcs_s_suffix':
        len_s_suffix= task["len_s_suffix"]            
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"    BOTH_valore_ottimo_task_{task_number}: {suff_from_pos[len(s)-len_s_suffix][0]}", file=fout)
            lcs = []
            reconstruct_opt_lcs_suff_from_pos(len(s)-len_s_suffix,0, lcs)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {lcs}", file=fout)
        return

    if task_codename == 'opt_lcs_t_suffix':
        len_t_suffix= task["len_t_suffix"]            
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"    BOTH_valore_ottimo_task_{task_number}: {suff_from_pos[0][len(t)-len_t_suffix]}", file=fout)
            lcs = []
            reconstruct_opt_lcs_suff_from_pos(0,len(t)-len_t_suffix, lcs)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {lcs}", file=fout)
        return

    
    if task_codename == 'opt_lcs_prefixes':
        len_s_prefix= task["len_s_prefix"]            
        len_t_prefix= task["len_t_prefix"]            
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {pref_of_len[len_s_prefix][len_t_prefix]}", file=fout)

            lcs = []
            reconstruct_opt_lcs_pref_of_len(len_s_prefix,len_t_prefix, lcs)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {list(reversed(lcs))}", file=fout)
        return
          
    if task_codename == 'opt_lcs_suffixes':
        len_s_suffix= task["len_s_suffix"]            
        len_t_suffix= task["len_t_suffix"]            
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"    BOTH_valore_ottimo_task_{task_number}: {suff_from_pos[len(s)-len_s_suffix][len(t)-len_t_suffix]}", file=fout)
            lcs = []
            reconstruct_opt_lcs_suff_from_pos(len(s)-len_s_suffix,len(t)-len_t_suffix, lcs)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {lcs}", file=fout)
        return
    

    if task_codename == 'opt_lcs_beginning':  #Fornire una massima sottosequenza comune tra  s  e  t che inizi con lettera o stringa prefisso dati
        beginning= task["beginning"]            
        i_s = -1
        i_t = -1
        for char in beginning:
            i_s += 1
            i_t += 1
            while s[i_s] != char:
                i_s += 1
                assert i_s < len(s)
            while t[i_t] != char:
                i_t += 1
                assert i_t < len(t)
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"    BOTH_valore_ottimo_task_{task_number}: {len(beginning)+suff_from_pos[i_s][i_t]}", file=fout)
            lcs = []
            reconstruct_opt_lcs_suff_from_pos(i_s,i_t, lcs)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {[char for char in beginning]+lcs}", file=fout)
        return
    
    if task_codename == 'opt_lcs_ending':  #Fornire una massima sottosequenza comune tra  s  e  t che finisca con un dato suffisso (ending)
        ending= task["ending"]            
        len_s = len(s)
        len_t = len(t)
        for char in reversed(ending):
            i_s -= 1
            i_t -= 1
            while s[len_s] != char:
                assert len_s > 0
                len_s -= 1
            while t[len_t] != char:
                assert len_t > 0
                len_t -= 1
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"    BOTH_valore_ottimo_task_{task_number}: {len(ending) + pref_of_len[len_s][len_t]}", file=fout)
            lcs = []
            reconstruct_opt_lcs_pref_of_len(len_s,len_t, lcs)
            print(f"\n    BOTH_soluzione_ottima_task_{task_number}: {list(reversed(lcs)) + [char for char in ending]}", file=fout)
        return
        
    print(f"ERROR: codename {task_codename} is an unknown codename for tasks!", sys.stderr)
    exit(1)


def put_standardized_items(tag, std_select, source_instance_dict, task_codename, task_number, fout):
    instance=source_instance_dict['instance']
    s= instance['s']
    t= instance['t']
    task=source_instance_dict['tasks'][task_number-1][task_number]
            
    if tag == "verif":
        if task_codename == 'opt_lcs_s_t':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_LCS(s, t, answer{num_of_question}, pt_green={task["ver_points"]}, pt_red={task["tot_points"]}, index_pt={num_of_question - 1}, val_or_sol="sol")))'""", file=fout)
                return
            
        if task_codename == 'opt_lcs_s_prefix':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_LCS("{s[:task["len_s_prefix"]]}", "{t}", answer{num_of_question}, pt_green={task["ver_points"]}, pt_red={task["tot_points"]}, index_pt={num_of_question - 1}, val_or_sol="sol")))'""", file=fout)
                return

        if task_codename == 'opt_lcs_t_prefix':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_LCS("{s}", "{t[:task["len_t_prefix"]]}", answer{num_of_question}, pt_green={task["ver_points"]}, pt_red={task["tot_points"]}, index_pt={num_of_question - 1}, val_or_sol="sol")))'""", file=fout)
                return

        if task_codename == 'opt_lcs_s_suffix':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_LCS("{s[len(s)-task["len_s_suffix"]:]}", "{t}", answer{num_of_question}, pt_green={task["ver_points"]}, pt_red={task["tot_points"]}, index_pt={num_of_question - 1}, val_or_sol="sol")))'""", file=fout)
                return

        if task_codename == 'opt_lcs_t_suffix':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_LCS("{s}", "{t[len(t)-task["len_t_suffix"]:]}", answer{num_of_question}, pt_green={task["ver_points"]}, pt_red={task["tot_points"]}, index_pt={num_of_question - 1}, val_or_sol="sol")))'""", file=fout)
                return

        if task_codename == 'opt_lcs_prefixes':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_LCS("{s[:task["len_s_prefix"]]}", "{t[:task["len_t_prefix"]]}", answer{num_of_question}, pt_green={task["ver_points"]}, pt_red={task["tot_points"]}, index_pt={num_of_question - 1}, val_or_sol="sol")))'""", file=fout)
                return

        if task_codename == 'opt_lcs_suffixes':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_LCS("{s[len(s)-task["len_s_suffix"]:]}", "{t[len(t)-task["len_t_suffix"]:]}", answer{num_of_question}, pt_green={task["ver_points"]}, pt_red={task["tot_points"]}, index_pt={num_of_question - 1}, val_or_sol="sol")))'""", file=fout)
                return

        if task_codename == 'opt_lcs_beginning':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_LCS(s, t, answer{num_of_question}, pt_green={task["ver_points"]}, pt_red={task["tot_points"]}, index_pt={num_of_question - 1}, val_or_sol="sol", start="{task["beginning"]}")))'""", file=fout)
                return

        if task_codename == 'opt_lcs_ending':
            if std_select == 'early_standard':
                print("""    verif: 'display(Markdown(verif_LCS(s, t, answer{num_of_question}, pt_green={task["ver_points"]}, pt_red={task["tot_points"]}, index_pt={num_of_question - 1}, val_or_sol="sol", end="{task["ending"]}")))'""", file=fout)
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

