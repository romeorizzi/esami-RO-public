#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors:
Verifiers: Alessandro Busatto, Paolo Graziani, Aurora Rossi, Davide Roznowicz;
Integration: Alice Raffaele, Romeo Rizzi.

"""

from sys import argv, exit, stderr
import os
import re
import yaml
from collections import OrderedDict
import nbformat as nb
import ast

import problems_common_lib as plib

PATH_UTILS = os.getcwd() + '/utils/'


def generate_nb(fullpath_yaml):
    # Notebook creation
    notebook = nb.v4.new_notebook()
    notebook['cells'] = []

    # Reading the instance
    exer = plib.read_exercise_yaml(fullpath_yaml)
    s=exer['instance']['s']
    forced_ele_pos=exer['instance']['forced_ele_pos']
    start_banned_interval=exer['instance']['start_banned_interval']
    end_banned_interval=exer['instance']['end_banned_interval']
    monotonicity_type_subtask1=exer['instance']['monotonicity_type_subtask1']
    monotonicity_type_subtask2=exer['instance']['monotonicity_type_subtask2']
    monotonicity_type_subtask3=exer['instance']['monotonicity_type_subtask3']
    monotonicity_type_subtask4=exer['instance']['monotonicity_type_subtask4']
    monotonicity_type_subtask5=exer['instance']['monotonicity_type_subtask5']
    
    tasks=exer['tasks']
    total_point=0
    n_tasks = 0
    for i in range(len(tasks)):
        total_point+=tasks[i][i+1]['tot_points']
        n_tasks += 1
    num_of_question=1

    yaml_gen=OrderedDict()
    yaml_gen['name']=exer['name']
    yaml_gen['title']=exer['title']
    yaml_gen['tags']=exer['tags']
    tasks_istanza_libera=[]

    # Heading and needed import
    plib.insert_user_bar_lib(notebook, run_cells=True)
    plib.insert_heading(notebook, exer['title'], run_cells=False) # heading with title
    plib.insert_import_mode_free(notebook, run_cells=False)
    plib.insert_n_tasks(notebook, n_tasks, run_cells=False)

    # BEGIN instance specific data pre-elaboration
    dictionary_of_types = {
         "SC": "<b>strettamente crescente</b>",
         "ND": "<b>non-decrescente</b>",
         "SD": "<b>strettamente decrescente</b>",
         "NC": "<b>non-crescente</b>",
          "V": "<b>una V-sequenza</b>, se cala fino ad un certo punto, e da l in poi cresce sempre",
          "A": "<b>ad A</b> (prima s e poi gi)</it>",
         "SV": "<b>a V stretto</b> <it>(prima strettamente gi e poi strettamente s)</it>",
         "SA": "<b>ad A stretta</b> <it>(prima strettamente s e poi strettamente gi)</it>",
          "N": "<b>una N-sequenza</b> (non-decrescente con al pi un ripensamento)</it>",
          "Z": "<b>una Z-sequenza</b> <it>(non-crescente con al pi un ripensamento)</it>",
         "SN": "<b>una N-sequenza stretta</b> <it>(strettamente crescente con al pi un ripensamento)</it>",
         "SZ": "<b>una Z-sequenza stretta</b> <it>(strettamente decrescente con al pi un ripensamento)</it>",
     "ZigZag": "<b>a Zig-Zag</b> <it>(primo passo a crescere e poi alterna ad ogni passo)</it>",
     "ZagZig": "<b>a Zag-Zig</b> <it>(primo passo a calare e poi alterna ad ogni passo)</it>",
    "ZigZagEQ": "<b>a Zig-Zag debole</b> <it>(primo passo a crescere e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>",
    "ZagZigEQ": "<b>a Zag-Zig debole</b> <it>(primo passo a calare e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>",
    "132-free": "<b>dal mondo delle permutazioni pattern free per un infinit di problemi in FPT</b>",
    }
    # END instance specific data pre-elaboration

    # Adding the instance to the notebook
    instance=f"""
    s={s}
    forced_ele_pos={forced_ele_pos}
    start_banned_interval={start_banned_interval}
    end_banned_interval={end_banned_interval}"""
    cell_string=instance
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ['noexport'], "trusted": True}
    plib.add_cell(notebook, cell_type='Code',data=cell_string,metadata=cell_metadata)

    # Verifier
    cell_string = """\
    def is_subseq(s, subs):
        found = 0
        pos_r = 0
        if len(subs)==0:
            return False
        else:
            while pos_r < len(s):
                if s[pos_r] == subs[found]:
                    found += 1
                    if found >= len(subs):
                        return True
                pos_r += 1
        return False

    def evaluation_format(answ, pt_green,pt_red, index_pt):
        pt_blue=0
        if pt_green!=0:
            pt_blue=pt_red-pt_green
            pt_red=0
        arr_point[index_pt]=pt_green
        file = open("points.txt", "w")
        file.write(str(arr_point))
        file.close()
        return f"{answ}. Totalizzeresti <span style='color:green'>[{pt_green} safe pt]</span>, \
                                        <span style='color:blue'>[{pt_blue} possible pt]</span>, \
                                        <span style='color:red'>[{pt_red} out of reach pt]</span>.<br>"
    
    
    # Legend of the possible sequence types:
    dictionary_of_types = {
          "SC": ("implemented", "<b>strettamente crescente</b>"),
          "ND": ("implemented", "<b>non-decrescente</b>"),
          "SD": ("implemented", "<b>strettamente decrescente</b>"),
          "NC": ("implemented", "<b>non-crescente</it>"),
           "V": ("implemented", "<b>a V</b> <it>(prima gi e poi s)</it>"),
           "A": ("implemented", "<b>ad A</b> (prima s e poi gi)</it>"),
          "SV": ("implemented", "<b>a V stretta</b> <it>(prima strettamente gi e poi strettamente s)</it>"),
          "SA": ("implemented", "<b>ad A stretta</b> <it>(prima strettamente s e poi strettamente gi)</it>"),
           "N": ("implemented", "<b>a N</b> (non-decrescente con al pi un ripensamento)</it>"),
           "Z": ("implemented", "<b>a Z</b> <it>(non-crescente con al pi un ripensamento)</it>"),
          "SN": ("implemented", "<b>a N stretta</b> <it>(strettamente crescente con al pi un ripensamento)</it>"),
          "SZ": ("implemented", "<b>a Z stretta</b> <it>(strettamente decrescente con al pi un ripensamento)</it>"),
      "ZigZag": ("implemented", "<b>a Zig-Zag</b> <it>(primo passo a crescere e poi alterna ad ogni passo)</it>"),
      "ZagZig": ("implemented", "<b>a Zag-Zig</b> <it>(primo passo a calare e poi alterna ad ogni passo)</it>"),
    "ZigZagEQ": ("implemented", "<b>a Zig-Zag debole</b> <it>(primo passo a crescere e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>"),
    "ZagZigEQ": ("implemented", "<b>a Zag-Zig debole</b> <it>(primo passo a calare e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>"),
    "132-free": ("not yet done", "<b>dal mondo delle permutazioni pattern free per un infinit di problemi in FPT</b>"),
         "...": ("not thought of yet", "<b>???</b>")
    }
    
    def Latex_type(seq_type):
        return dictionary_of_types[seq_type][1].replace("_", "\_")
    
    
    def is_seq_of_type(s, name_s, seq_type):
        first_down = first_up = first_flat = None
        for i in range(1,len(s)):
            if s[i] < s[i-1]:
                if seq_type=="V" and first_up != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type('V')} poich ${LaTexVarName(name_s)}[${i-1}$] = {s[i-2]} $<$ {s[i-1]} $= {LaTexVarName(name_s)}[${i}$] > {LaTexVarName(name_s)}[${i+1}$] =$ {s[i]}.")
                if seq_type in {"SC","ND"} or (seq_type in {"ZigZag","ZigZagEQ"} and s[i]%2 == 1) or (seq_type in {"ZagZig","ZagZigEQ"} and s[i]%2 == 0):
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${i}$] $= {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if first_down == None:
                    first_down = i
                elif seq_type=="N":
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${first_down}$] = {s[first_down-1]} $>$ {s[first_down]} $= {LaTexVarName(name_s)}[${first_down+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if seq_type=="SN" and first_flat != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${first_flat}$] = {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")                
            if s[i] > s[i-1]:
                if seq_type=="A" and first_down != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type('A')} poich ${LaTexVarName(name_s)}[${i-1}$] =$ {s[i-2]} $>$ {s[i-1]} $= {LaTexVarName(name_s)}[${i}$] < {LaTexVarName(name_s)}[${i+1}$] =$ {s[i]}.")
                if seq_type in {"SD","NC"} or (seq_type in {"ZagZig","ZagZigEQ"} and s[i]%2 == 1) or (seq_type in {"ZigZag","ZigZagEQ"} and s[i]%2 == 0):
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $<$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if first_up == None:
                    first_up = i
                elif seq_type=="Z":
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${first_up}$] =$ {s[first_up-1]} $<$ {s[first_up]} $= {LaTexVarName(name_s)}[${first_up+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $<$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if seq_type=="SZ" and first_flat != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${first_flat}$] =$ {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $<$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if s[i] == s[i-1]:
                if seq_type in {"SC","SD","SV","SA","ZigZag","ZagZig"}:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if first_flat == None:
                    first_flat = i
                elif seq_type in {"SN","SZ"}:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${first_flat}$] =$ {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if seq_type=="SN" and first_down != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${first_down}$] =$ {s[first_down-1]} $>$ {s[first_down]} $= {LaTexVarName(name_s)}[${first_down+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if seq_type=="SZ" and first_up != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non  di tipo {Latex_type(seq_type)} poich ${LaTexVarName(name_s)}[${first_up}$] =$ {s[first_up-1]} $<$ {s[first_up]} $= {LaTexVarName(name_s)}[${first_up+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
        return (1,None)
    
    def LaTexVarName(var_name):
        return var_name.replace("_", "\_")
    
    
    def is_subseq_of_type(s, name_s, subs, name_subs, subs_type, pt_green, pt_red, index_pt, forced_ele_pos = None, start_banned_interval = None, end_banned_interval = None):
        submission_string = f"Hai inserito il certificato ${LaTexVarName(name_subs)}={subs}$."
        submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"
    
        if not is_seq_of_type(subs, "subs", subs_type)[0]:
            return submission_string + evaluation_format("No", 0,pt_red, index_pt) + is_seq_of_type(subs, "subs", subs_type)[1]
        if start_banned_interval != None or end_banned_interval != None:
            assert start_banned_interval != None and end_banned_interval != None
            if forced_ele_pos != None:
                assert forced_ele_pos < start_banned_interval or forced_ele_pos > end_banned_interval
                if forced_ele_pos > end_banned_interval:
                    forced_ele_pos -= end_banned_interval 
            aux = s[:start_banned_interval-1] +s[end_banned_interval:]
        if not is_subseq(s, subs):
            return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non  sottosequenza di ${LaTexVarName(name_s)}$."
        if forced_ele_pos != None:
            forced_ele_0basedpos = forced_ele_pos-1
            found_magic_point = False
            for guess_0basedpos_in_subs in range(len(subs)):
                if subs[guess_0basedpos_in_subs] == s[forced_ele_0basedpos]:
                    if is_subseq(s[:forced_ele_0basedpos], subs[:guess_0basedpos_in_subs]) and is_subseq(s[forced_ele_0basedpos:], subs[guess_0basedpos_in_subs:]):
                        found_magic_point = True#False
            if not found_magic_point:
                return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non  sottosequenza di ${LaTexVarName(name_s)}$ che ne includa l'elemento in posizione ${forced_ele_pos}$."
    
        return submission_string + f"{evaluation_format('Ammissibile', pt_green,pt_red, index_pt)}"
    
    def eval_coloring(s, name_s, col, name_col, subs_type, pt_green, pt_red, index_pt):
        submission_string = f"Hai inserito il certificato ${LaTexVarName(name_col)}={col}$."
        submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"
        if len(col)!=len(s):
            if len(col)>len(s):
                return f"{evaluation_format('No', 0,pt_red,index_pt)}"+f"La sequenza da te data  pi lunga dell'istanza di {len(col)-len(s)}, deve essere lunga come quella di input."
            if len(col)<len(s):
                return f"{evaluation_format('No', 0,pt_red,index_pt)}"+f"La sequenza da te data deve essere lunga come quella di input: mancano {len(s)-len(col)} elementi."
        else:
            for c in col:
                subs = [s[i] for i in range(len(s)) if col[i] == c]
                if not is_seq_of_type(subs, "subs", subs_type)[0]:
                    return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"Controllando la sottosequenza degli elementi colorati con il colore: {c} in ${LaTexVarName(name_s)}$, cio: {subs} ... " + is_seq_of_type(subs, "subs", subs_type)[1]        
        return submission_string + f"{evaluation_format('Ammissibile', pt_green ,pt_red, index_pt)}"
    
    def min_subs_of_type(s, name_s, subs, name_subs, subs_type, pt_green, pt_red, index_pt):
        submission_string = f"Hai inserito il certificato ${LaTexVarName(name_subs)}={subs}$."
        submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"
    
        check={}
        for n in s:
            if n not in check.keys():
                check[n]=1
            else:
                check[n]=check[n]+1
        for elem in subs:
            for n in elem:
                if n in check.keys():
                    check[n]=check[n]-1
        for key in check.keys():
            if check[key] != 0:
                return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"Le tue sottosequenze non contengono tutti i valori di ${name_s}$"
        for elem in subs:
            if not is_seq_of_type(elem, "subs", subs_type)[0]:
                return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"Attenzione la sottosequenza ${elem}$ non  del tipo richiesto."
        return submission_string + f"{evaluation_format('Ammissibile', pt_green,pt_red,index_pt)}"
    """
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ['noexport'], "trusted": True}
    plib.add_cell(notebook, cell_type="Code",data=cell_string,metadata=cell_metadata)

    # Description1
    cell_string="Si consideri la seguente sequenza di numeri naturali:<br/><br/>"+str(s)
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "trusted": True}
    plib.add_cell(notebook, cell_type='Markdown',data=cell_string,metadata=cell_metadata)
    yaml_gen['description1']=cell_string


    # Requests
    for i in range(len(tasks)):
        task=tasks[i][i+1]
        if 'request_txt' in task.keys():
            fstring= task['request_txt']
            request_txt= eval(f"f'{fstring}'")
        if 'request' in task.keys():
            fstring= task['request']
            request= eval(f"f'{fstring}'")
        if not 'request_txt' in task.keys():
            request_txt= request
        if not 'request' in task.keys():
            request= request_txt
        tasks_istanza_libera.append({1+len(tasks_istanza_libera):{'tot_points' : task['tot_points'],'ver_points': task['ver_points'], 'description1': request_txt}})
        request_full= f"__Richiesta {i+1} [{task['tot_points']} punti]__: " + request
        
        # Single request text cell:
        cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "tags": ['runcell','noexport'], "trusted": True}
        plib.add_cell(notebook, cell_type='Markdown', data=request_full, metadata=cell_metadata)

        # Single request answer cell:
        answer_cell_type = 'Code'
        if 'answer_cell_type' in task.keys():
            answer_cell_type = task['answer_cell_type']
        fstring= ""
        if 'init_answ_cell_msg' in task.keys():
            fstring= task['init_answ_cell_msg']
        init_answ_cell_msg= eval(f"f'{fstring}'")
        cell_metadata={"init_cell": True, "trusted": True, "deletable": False}
        plib.add_cell(notebook,cell_type='Code',data=init_answ_cell_msg,metadata=cell_metadata)
        
        # Single request verifier cell:
        if 'verif' in task.keys():
            fstring= task['verif']
            verif= eval(f"f'{fstring}'")
            cell_metadata={"init_cell": True, "hide_input": True, "editable": False, "deletable": False, "trusted": True}
            plib.add_cell(notebook,cell_type='Code',data=verif,metadata=cell_metadata)
        num_of_question += 1
    
    
    yaml_gen['tasks']=tasks_istanza_libera
    return notebook, yaml_gen


    # TRACCIA DELLE IMPOSTAZIONI PRIMA DELL'UNIFICAZIONE
        # Single request text cell:
        # cell_metadata ={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "trusted": True}

        # Single request answer cell: (except for R0)
        # cell_metadata={"init_cell": True, "trusted": True, "deletable": False}
        # Single request verifier cell:
        # cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "trusted": True}
