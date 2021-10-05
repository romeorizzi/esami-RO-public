#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import re
from pprint import pprint

INFO_UNIVERSE = {'instance_design','eval_support','feedback','explanations','resolving_code'}
    
CATEGORY='dp_poldo'
def usage():
    print(f"""This script ({sys.argv[0]}) serves in the generation process of problems in the category '{CATEGORY}'. It mainly generates a full source yaml file problem starting from a tiny yaml file containing only the instance (specifically encoded as for problems of the '{CATEGORY}' category). The generated file can be used as the source for the later generation of the Jupyter notebooks or others formats in which the exercises or parts of them are actually rendered. Some of these formats are meant to support features like contextual assistance to the student (during the the exam or when training) or related activities like evaluation and grading work.

Right now, this script requires precisely one argument. The unique argument to this script should be the fullname of the .instance file containing an instance for problem {CATEGORY}. Right now this fullname is expected to have .instance as extension!

Right now the script writes down on stdout the extended yaml file including the additional authomatically generated fields offering the support information for the specific fields and for the field categories that have been required (support in the evaluation process, explanations or feedback to the students, instance design).

Usage example:
   ${sys.argv[0]} ../../collections/RO-2021-06-18/dp_poldo/01/dp_poldo.instance

The file ../../collections/RO-2021-06-18/dp_poldo/01/dp_poldo.instance is only required to contain the `instance` field with the instance defining data for problem category {CATEGORY}.

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

def sol_right_wing(pos, monotonia, dp_array, faces_array):
    assert 0 <= pos < len(dp_array)==len(faces_array)
    assert dp_array[pos] > 0
    if dp_array[pos] == 1:
        return [faces_array[pos]]
    next_pos = pos+1
    while next_pos < len(dp_array):
        if dp_array[next_pos] != dp_array[pos]-1:
            next_pos += 1
        elif faces_array[pos] > faces_array[next_pos] and monotonia in {'SC','ND'}:
            next_pos += 1
        elif faces_array[pos] < faces_array[next_pos] and monotonia in {'SD','NC'}:
            next_pos += 1
        elif faces_array[pos] == faces_array[next_pos] and monotonia in {'SC','SD'}:
            next_pos += 1
        else:
            return [faces_array[pos]] + sol_right_wing(next_pos, monotonia, dp_array, faces_array)
    assert False
            
def sol_left_wing(pos, monotonia, dp_array, faces_array):
    assert 0 <= pos < len(dp_array)==len(faces_array)
    assert dp_array[pos] > 0
    if dp_array[pos] == 1:
        return [faces_array[pos]]
    next_pos = pos-1
    while next_pos < len(dp_array):
        if dp_array[next_pos] != dp_array[pos]-1:
            next_pos -= 1
        elif faces_array[next_pos] > faces_array[pos] and monotonia in {'SC','ND'}:
            next_pos -= 1
        elif faces_array[next_pos] < faces_array[pos] and monotonia in {'SD','NC'}:
            next_pos -= 1
        elif faces_array[next_pos] == faces_array[pos] and monotonia in {'SC','SD'}:
            next_pos -= 1
        else:
            return  sol_left_wing(next_pos, monotonia, dp_array, faces_array) + [faces_array[pos]]
    assert False
            
    
def yield_info_addenda(source_instance_dict, task_codename, task_number, turned_off_info, fout):
    addenda = INFO_UNIVERSE - turned_off_info
    instance=source_instance_dict['instance']
    s= instance['s']
    forced_ele_pos= instance['forced_ele_pos']
    start_banned_interval= instance['start_banned_interval']
    end_banned_interval= instance['end_banned_interval']
    task=source_instance_dict['tasks'][task_number-1][task_number]

    """ an hardcoded instance used for debugging and fast prototyping:
    s= [60, 20, 54, 82, 7, 9, 25, 13, 31, 47, 70, 83, 4, 32, 16, 61, 43, 20, 15, 54, 63, 99, 43, 13, 28]
    forced_ele_pos= 15 # posizione dell'elemento che deve essere incluso nella sottosequenza (per le posizioni parti a contare da 1)
    start_banned_interval= 5 # prima posizione bannata da intervallo proibito
    end_banned_interval=   8 # ultima posizione bannata
    """

    dual = {'SC': 'NC', 'NC': 'SC', 'SD': 'ND', 'ND' : 'SD'}
    monotonia=task_codename.split("_")[0]
    if task_codename.split("_")[1] == 'cover':
        monotonia=dual[monotonia]
    if monotonia=='A':
        monotonia_at_left = 'SC'
        monotonia_at_right = 'SD'
    elif monotonia=='V':
        monotonia_at_left = 'SD'
        monotonia_at_right = 'SC'
    elif len(monotonia)==5 and monotonia[2]=='-':
        monotonia_at_left = monotonia[:2]
        monotonia_at_right = monotonia[3:]
    else:
        monotonia_at_left = monotonia_at_right = monotonia
    
    max_terminating_with_ele_at_pos = [ 1 ] * len(s)
    max_terminating_not_later_than_at_pos = [ 1 ] * len(s)
    pos_max_terminating_not_later_than_at_pos = [ 0 ] * len(s)
    for i in range(len(s)):
        for j in range(i):
          if (s[j]<s[i] and monotonia_at_left in {'SC','ND'}) or (s[j]>s[i] and monotonia_at_left in {'SD','NC'}) or (s[j]==s[i] and monotonia_at_left in {'NC','ND'}):
              max_terminating_with_ele_at_pos[i] = max(max_terminating_with_ele_at_pos[i], 1 + max_terminating_with_ele_at_pos[j])
        if i > 0:
            max_terminating_not_later_than_at_pos[i] = max_terminating_not_later_than_at_pos[i-1]
            pos_max_terminating_not_later_than_at_pos[i] = pos_max_terminating_not_later_than_at_pos[i-1]
            if max_terminating_with_ele_at_pos[i] > max_terminating_not_later_than_at_pos[i]:
                max_terminating_not_later_than_at_pos[i] = max_terminating_with_ele_at_pos[i]
                pos_max_terminating_not_later_than_at_pos[i] = i
              
    if task_codename.split("_")[0] in dual and task_codename.split("_")[1]=='subseq' and task_codename.split("_")[2]=='free':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_terminating_not_later_than_at_pos[len(s)-1]}", file=fout)
            opt_sol = sol_left_wing(pos_max_terminating_not_later_than_at_pos[len(s)-1], monotonia_at_left, dp_array=max_terminating_with_ele_at_pos, faces_array=s)
            print(f"\n    BOTH_una_soluzione_ottima_task_{task_number}: {opt_sol}", file=fout)
        if 'explantions' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
            print("     Definiamo i vettori `max_terminating_with_ele_at_pos` e `max_terminating_not_later_than_at_pos` entrambi di lunghezza |s| ed indicizzati dalle posizioni degli elementi in s. Quì `max_terminating_with_ele_at_pos`[i] = massima lunghezza di una sottosequenza di s con la monotona richiesta e che termina proprio con l'i-esimo elemento di s. Invece `max_terminating_not_later_than_at_pos`[i] = massima lunghezza di una sottosequenza di s correttamente monotona e che non prende da s elementi successivi all'i-esimo elemento. Una computazione ricorsiva prefissa produce facilmente `max_terminating_not_later_than_at_pos` poggiando su `max_terminating_with_ele_at_pos`, ma in realtà anche i valori in `max_terminating_not_later_than_at_pos` finiscono computati ricorsivamente (anche se con lavoro quadratico invece che lineare) e cadono come i birilli. Si ispezionino quindi i seguenti vettori, computati entrambi da sinista, e conteneti risposte a tutta una famiglia di domande di nostra pertinenza.", file=fout)
            print("    AUX__Stampa dei vettori `max_terminating_with_ele_at_pos` e `max_terminating_not_later_than_at_pos`:", file=fout)
            print("    ",end=" ", file=fout)
            for i in range(len(s)):
                print(f"{s[i]:2}", end=" ", file=fout)
            print("(sequence s)", file=fout)
            print("    ",end=" ", file=fout)
            for i in range(len(s)):
                print(f"{max_terminating_with_ele_at_pos[i]:2}", end=" ", file=fout)
            print("(max_terminating_with_ele_at_pos)", file=fout)
            print("    ",end=" ", file=fout)
            for i in range(len(s)):
                print(f"{max_terminating_not_later_than_at_pos[i]:2}", end=" ", file=fout)
            print("(max_terminating_not_later_than_at_pos)", file=fout)
            print("    ",end=" ", file=fout)
            for i in range(len(s)):
                print(f"{pos_max_terminating_not_later_than_at_pos[i]:2}", end=" ", file=fout)
            print("(pos_max_terminating_not_later_than_at_pos)", file=fout)
        return
            
    if task_codename.split("_")[1]=='cover':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
             print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_terminating_not_later_than_at_pos[len(s)-1]}, una colorazione ottima è {max_terminating_with_ele_at_pos}", file=fout)
        return
             
    max_beginning_with_ele_at_pos = [ 1 ] * len(s)
    max_beginning_not_before_than_pos = [ 1 ] * len(s)
    pos_max_beginning_not_before_than_pos = [ len(s)-1 ] * len(s)
    for i in range(len(s)-1,-1,-1):
        for j in range(i+1,len(s)):
          if (s[j]>s[i] and monotonia_at_right in {'SC','ND'}) or (s[j]<s[i] and monotonia_at_right in {'SD','NC'}) or (s[j]==s[i] and monotonia_at_right in {'NC','ND'}):
              max_beginning_with_ele_at_pos[i] = max(max_beginning_with_ele_at_pos[i], 1 + max_beginning_with_ele_at_pos[j])
        if i < len(s)-1:      
            max_beginning_not_before_than_pos[i] = max_beginning_not_before_than_pos[i+1]
            pos_max_beginning_not_before_than_pos[i] = pos_max_beginning_not_before_than_pos[i+1]
            if max_beginning_with_ele_at_pos[i] > max_beginning_not_before_than_pos[i]:
                max_beginning_not_before_than_pos[i] = max_beginning_with_ele_at_pos[i]
                pos_max_beginning_not_before_than_pos[i] = i
              
    max_ext = 0
    i_max=None
    j_max=None
    for i in range(start_banned_interval):
        for j in range(1+end_banned_interval,len(s)):
            if (s[j]>s[i] and monotonia in {'SC','ND'}) or (s[j]<s[i] and monotonia in {'SD','NC'}) or (s[j]==s[i] and monotonia in {'NC','ND'}):
                if max_terminating_with_ele_at_pos[i] + max_beginning_with_ele_at_pos[j] > max_ext:
                    max_ext=max_terminating_with_ele_at_pos[i] + max_beginning_with_ele_at_pos[j]
                    i_max= i
                    j_max=j
            if max_terminating_with_ele_at_pos[i] > max_ext:
                max_ext=max_terminating_with_ele_at_pos[i]
                i_max= i
                j_max=None
            if max_beginning_with_ele_at_pos[j] > max_ext:
                max_ext=max_beginning_with_ele_at_pos[j]
                i_max= None
                j_max=j

    if task_codename.split("_")[-1]=='banned-interval':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_ext}", file=fout)
            if i_max == None:
                opt_sol = sol_right_wing(j_max, monotonia, dp_array=max_beginning_with_ele_at_pos, faces_array=s)
                print(f"\n    BOTH_una_soluzione_ottima_task_{task_number}: {opt_sol}  (nota: quì il primo elemento preso viene dopo la fine di intervallo interdetto.)", file=fout)            
            elif j_max == None:
                opt_sol = sol_left_wing(i_max, monotonia, dp_array=max_terminating_with_ele_at_pos, faces_array=s)
                print(f"\n    BOTH_una_soluzione_ottima_task_{task_number}: {opt_sol}  (nota: quì lo ultimo elemento preso viene prima di intervallo interdetto. ", file=fout)            
            else:
                opt_sol = sol_left_wing(i_max, monotonia, dp_array=max_terminating_with_ele_at_pos, faces_array=s) + sol_right_wing(j_max, monotonia, dp_array=max_beginning_with_ele_at_pos, faces_array=s)
                print(f"\n    BOTH_una_soluzione_ottima_task_{task_number}: {opt_sol}", file=fout)            
            dests = []
            if 'instance_design' in addenda or 'eval_support' in addenda:
                dests.append('PRIV_')
            if 'feedback' in addenda or 'explanations' in addenda:
                dests.append('AUXS_')
            for dest in dests:
                if i_max == None:
                    print(f"\n    {dest}valore_ottimo_task_{task_number}: max={max_ext}, il primo elemento preso viene dopo la fine dell'intervallo interdetto. E più precisamente è {j_max} (val={max_beginning_with_ele_at_pos[j_max]}).", file=fout)
                elif j_max == None:
                    print(f"\n    {dest}valore_ottimo_task_{task_number}: max={max_ext}, l'ultimo elemento preso viene prima dell'intervallo interdetto. E più precisamente è {i_max} (val={max_terminating_with_ele_at_pos[i_max]}).", file=fout)
                else:
                    print(f"\n    {dest}valore_ottimo_task_{task_number}: max={max_ext}, ultimo elemento preso prima di intervallo interdetto ha indice {i_max} (e valore {max_terminating_with_ele_at_pos[i_max]}), primo elemento preso dopo intervallo interdetto ha indice {j_max} (e valore {max_beginning_with_ele_at_pos[j_max]})", file=fout)
            if 'feedback' in addenda or 'explanations' in addenda:
                print(f"\n    AUX__spiegazione_task_{task_number}: |", file=fout)
                print("     Definiamo i vettori `max_beginning_with_ele_at_pos` e `max_beginning_not_before_than_pos` entrambi di lunghezza |s| ed indicizzati dalle posizioni degli elementi in s. Quì `max_beginning_with_ele_at_pos`[i] = massima lunghezza di una sottosequenza strettamente crescente di s che cominci proprio con l'i-esimo elemento di s. Invece `max_beginning_not_before_than_pos`[i] = massima lunghezza di una sottosequenza strettamente crescente che non prende da s elementi precedenti l'i-esimo elemento. Una computazione ricorsiva, ora suffissa ma in tutto simmetrica alla precendente, produce facilmente i valori di `max_beginning_not_before_than_pos` e di `max_beginning_with_ele_at_pos` procedendo ordinatamente da destra verso sinistra. Esplorando tali vettori, congiuntamente ai prcednti, diviene possibile rispondere alle Richieste 2, 3 e 4.", file=fout)
                print("    AUX__Stampa dei vettori `max_beginning_with_ele_at_pos` e `max_beginning_not_before_than_pos`:", file=fout)
                print("    ",end=" ", file=fout)
                for i in range(len(s)):
                    print(f"{s[i]:2}", end=" ", file=fout)
                print("(sequence s)", file=fout)
                print("    ",end=" ", file=fout)
                for i in range(len(s)):
                    print(f"{max_beginning_with_ele_at_pos[i]:2}", end=" ", file=fout)
                print("(max_beginning_with_ele_at_pos)", file=fout)
                print("    ",end=" ", file=fout)
                for i in range(len(s)):
                    print(f"{max_beginning_not_before_than_pos[i]:2}", end=" ", file=fout)
                print("(max_beginning_not_before_than_pos)", file=fout)
                print("    ",end=" ", file=fout)
                for i in range(len(s)):
                    print(f"{pos_max_beginning_not_before_than_pos[i]:2}", end=" ", file=fout)
                print("(pos_max_beginning_not_before_than_pos)", file=fout)
        return

    if task_codename.split("_")[-1]=='forced-element':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_terminating_with_ele_at_pos[forced_ele_pos-1] + max_beginning_with_ele_at_pos[forced_ele_pos-1] -1}", file=fout)
            opt_sol = sol_left_wing(forced_ele_pos-1, monotonia, dp_array=max_terminating_with_ele_at_pos, faces_array=s)[:-1] + sol_right_wing(forced_ele_pos-1, monotonia, dp_array=max_beginning_with_ele_at_pos, faces_array=s)
            print(f"\n    BOTH_una_soluzione_ottima_task_{task_number}: {opt_sol}", file=fout)            
            print(f"\n    PRIV_valore_ottimo_task_{task_number}: {max_terminating_with_ele_at_pos[forced_ele_pos-1] + max_beginning_with_ele_at_pos[forced_ele_pos-1] -1} (dato da max_terminating_with_ele_at_pos[{forced_ele_pos-1}] + max_beginning_with_ele_at_pos[{forced_ele_pos-1}] -1)", file=fout)
            print(f"\n    AUXS_valore_ottimo_task_{task_number}: {max_terminating_with_ele_at_pos[forced_ele_pos-1] + max_beginning_with_ele_at_pos[forced_ele_pos-1] -1} (dato da max_terminating_with_ele_at_pos[{forced_ele_pos-1}] + max_beginning_with_ele_at_pos[{forced_ele_pos-1}] -1)", file=fout)
        return

    if task_codename.split("_")[1]=='subseq' and task_codename.split("_")[2]=='free':
        if 'instance_design' in addenda or 'eval_support' in addenda or 'feedback' in addenda:
            if task_codename.split("_")[0] in {'A','V'}:
                i_max=0
                max_val = 0
                for i in range(len(s)):
                    if max_val < max_terminating_with_ele_at_pos[i] + max_beginning_with_ele_at_pos[i] -1:
                        max_val = max_terminating_with_ele_at_pos[i] + max_beginning_with_ele_at_pos[i] -1
                        i_max=i
                print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_val}, indice di ultimo elemento del primo run = {i_max}", file=fout)
                #print(f"i_max={i_max}\nmax_terminating_with_ele_at_pos={max_terminating_with_ele_at_pos}\n                              s={s}\n  max_beginning_with_ele_at_pos={max_beginning_with_ele_at_pos}")
                opt_sol = sol_left_wing(i_max, monotonia_at_left, dp_array=max_terminating_with_ele_at_pos, faces_array=s)[:-1] + sol_right_wing(i_max, monotonia_at_right, dp_array=max_beginning_with_ele_at_pos, faces_array=s)
                print(f"\n    BOTH_una_soluzione_ottima_task_{task_number}: {opt_sol}", file=fout)
                print(f"    AUX__spiegazione_task_{task_number}: |", file=fout)
                if task_codename.split("_")[0] == 'V':
                    print("     La risposta è data da max_i max_strictly_decreasing_terminating_with_ele_at_pos[i] + max_strictly_increasing_beginning_with_ele_at_pos[i] -1", file=fout)
                elif task_codename.split("_")[0] == 'A':
                    print("     La risposta è data da max_i max_strictly_increasing_terminating_with_ele_at_pos[i] + max_strictly_decreasing_beginning_with_ele_at_pos[i] -1", file=fout)
            elif task_codename.split("_")[0]=='Z':
                max_val = 1
                i_max=0
                for i in range(len(s)-1):
                    if max_val < max_terminating_not_later_than_at_pos[i] + max_beginning_not_before_than_pos[i+1]:
                            max_val = max_terminating_not_later_than_at_pos[i] + max_beginning_not_before_than_pos[i+1]
                            i_max=i
                print(f"\n    BOTH_valore_ottimo_task_{task_number}: {max_val}, indice di ultimo elemento del primo run = {i_max}", file=fout)
                opt_sol = sol_left_wing(pos_max_terminating_not_later_than_at_pos[i_max], monotonia, dp_array=max_terminating_with_ele_at_pos, faces_array=s) + sol_right_wing(pos_max_beginning_not_before_than_pos[i_max+1], monotonia, dp_array=max_beginning_with_ele_at_pos, faces_array=s)
                print(f"\n    BOTH_una_soluzione_ottima_task_{task_number}: {opt_sol}", file=fout)            
                print(f"    AUX__spiegazione_task_{task_number}: |", file=fout)
                print("     La risposta è data da max_i max_terminating_not_later_than_at_pos[i] + max_beginning_not_before_than_pos[i+1]", file=fout)
        return

    print(f"ERROR: codename {task_codename} is an unknown codename for tasks!", file=sys.stderr)
    exit(1)


def put_standardized_items(tag, std_select, source_instance_dict, task_codename, task_number, fout):
    instance=source_instance_dict['instance']
    s= instance['s']
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

