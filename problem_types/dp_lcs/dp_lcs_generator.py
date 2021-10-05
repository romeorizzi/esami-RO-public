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
    s = exer['instance']['s']
    t = exer['instance']['t']
    
    tasks=exer['tasks']
    total_point=0
    n_tasks = 0
    for i in range (len(tasks)):
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
    plib.insert_heading(notebook, exer['title'], run_cells=True) # heading with title
    plib.insert_import_mode_free(notebook, run_cells=True)
    plib.insert_n_tasks(notebook, n_tasks, run_cells=True)
    
    # Adding s and t in the notebook
    cell_type = 'Code'
    cell_string = f"""\
    s = "{s}"
    t = "{t}"
    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport'],
                     "trusted": True}
    plib.add_cell(notebook,cell_type, cell_string, cell_metadata)

    # Verifier
    cell_type = "Code"
    cell_string = """\
    def is_sub(sub,string):
        match=0
        i=0
        j=0
        sol=True
        while match<len(sub) and i<len(string):
            if string[i]==sub[j]:
                match+=1
                if j<len(sub)-1:
                    j+=1
            i+=1
        if match!=len(sub):
            sol=False
        return sol

    def verif_LCS(string1, string2, answer, pt_green, pt_red, index_pt, val_or_sol="sol", start=False, end=False):
        if answer=="":
            return evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita è vuota."
        if val_or_sol=="val":
            if type(answer)==int:
                return evaluation_format("Si", 1,pt_red,index_pt)+"Hai immesso un intero come richiesto. (Ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto.)"
            else:
                return evaluation_format("No", 0,pt_red,index_pt)+"A questa domanda è richiesto si risponda con un intero."
        if start != False and answer[:len(start)]!=start:
            return evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita non inizia con __{start}__."
        if end != False and (len(answer)<len(end) or answer[len(answer)-len(end):]!=end):
            return evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita non termina con __{end}__."
        if not is_sub(answer,string1):
            return evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita non è una sottosequenza di {string1}."
        if not is_sub(answer,string2):
            return evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita non è una sottosequenza di {string2}."
        s = ' ' + string1 
        t = ' ' + string2
        n = len(s)
        m = len(t)
        L = np.zeros((n, m)) 
        for i in range(1,n):
            for j in range(1,m):
                if s[i] == t[j]: 
                    L[i][j] = L[i-1][j-1] + 1
                else: 
                    L[i][j] = max(L[i-1][j], L[i][j-1]) 
        correct_len=np.max(L)
        return evaluation_format("Si", pt_green, pt_red, index_pt)+"La sottosequenza fornita è ammissibile."

    
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

    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport'],
                     "trusted": True}
    plib.add_cell(notebook, cell_type, cell_string, cell_metadata)

    # Description1
    cell_type = 'Markdown'
    cell_string = "Si considerino le seguenti sequenze di caratteri:<br/><br/> $s$ = " + str(s) + "<br/>  $t$ = " + str(t)
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": [],
                     "trusted": True}
    plib.add_cell(notebook,cell_type, cell_string, cell_metadata)
    yaml_gen['description1'] = cell_string
    
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
        plib.add_cell(notebook, cell_type=answer_cell_type, data=init_answ_cell_msg, metadata=cell_metadata)
        
        # Single request verifier cell:
        if 'verif' in task.keys():
            fstring= task['verif']
            verif= eval(f"f'{fstring}'")
            cell_metadata={"init_cell": True, "hide_input": True, "editable": False, "deletable": False, "trusted": True}
            plib.add_cell(notebook, cell_type='Code', data=verif, metadata=cell_metadata)
        num_of_question += 1
    
    
    yaml_gen['tasks']=tasks_istanza_libera
    return notebook, yaml_gen


    # TRACCIA DELLE IMPOSTAZIONI DIVERSE PRIMA DELL'UNIFICAZIONE
        # Single request text cell:
        # cell_metadata ={"hide_input": True, "init_cell": True, "editable": False,  "deletable": False, "tags": [], "trusted": True}

        # Single request answer cell: (except for R0)
        # cell_metadata={"init_cell": True, "trusted": True, "deletable": False}
    
