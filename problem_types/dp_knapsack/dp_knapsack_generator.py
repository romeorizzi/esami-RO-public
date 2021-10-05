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


def usage():
    print(f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml>  il nome del file coi dati di istanza specifica.""", file=stderr)

    
def generate_nb(fullpath_yaml):
   # Notebook creation
    notebook = nb.v4.new_notebook()
    notebook['cells'] = []
    
    # Reading the instance
    exer = plib.read_exercise_yaml(fullpath_yaml)
    CapacityMax=exer['instance']['CapacityMax']
    elementi=exer['instance']['elementi']
    pesi=exer['instance']['pesi']
    valori=exer['instance']['valori']
    
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
    plib.insert_user_bar_lib(notebook, run_cells=False)
    plib.insert_heading(notebook, exer['title'], run_cells=False) # heading with title
    plib.insert_import_mode_free(notebook, run_cells=False)
    plib.insert_n_tasks(notebook, n_tasks, run_cells=False)
    
    # Knapsack
    cell_string=f"""
    elementi= {elementi}
    pesi = {pesi}
    valori = {valori}
    CapacityMax= {CapacityMax}

    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport'], "trusted": True}
    plib.add_cell(notebook, cell_type='Code',data=cell_string,metadata=cell_metadata)

    # Verifier
    cell_string= """\
    import copy
    
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
    
    def verif_knapsack(elementi,pesi, valori, Capacity,answer,pt_green,pt_red, index_pt, val_or_sol="sol",edr=False):
        elementi2=copy.deepcopy(elementi)
        pesi2=copy.deepcopy(pesi)
        valori2=copy.deepcopy(valori)
        if edr!=False:
            for elemento in edr:
                i=elementi2.index(elemento)
                elementi2.pop(i)
                pesi2.pop(i)
                valori2.pop(i)
            
        n = len(pesi2)
        S = [[0 for j in range(Capacity+1)] for i in range(n)] 
        for i in range(1,n):
            for j in range(Capacity+1):
                S[i][j] = S[i-1][j]
                if pesi2[i] <= j and S[i-1][j-pesi2[i]] + valori2[i] > S[i][j]:
                    S[i][j] = S[i-1][j-pesi2[i]] + valori2[i]
        max_val=S[-1][-1]
        if val_or_sol=="val":
            if type(answer)==int:
                return evaluation_format("Si", 1,pt_red,index_pt)+"Hai immesso un intero come richiesto. (Ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto.)"
            else:
                return evaluation_format("No", 0,pt_red,index_pt)+"A questa domanda è richiesto si risponda con un intero."
        if val_or_sol=="sol":
            if type(answer)==list:
                sum_valori=0
                sum_pesi=0
                for i in range(len(answer)):
                    sum_valori+=valori2[elementi.index(answer[i])]
                    sum_pesi+=pesi2[elementi.index(answer[i])]
                if sum_pesi<=Capacity:
                    return evaluation_format("Si", 1,pt_red,index_pt)+"Il sottoinsieme di elementi è ammissibile. (Ovviamente durante lo svolgimento dell'esame non posso dirti se sia anche ottimo.)"
                else:
                    return evaluation_format("No", 0,pt_red,index_pt)+f"Il sottoinsieme di elementi NON è ammissibile in quanto la somma dei loro pesi è {sum_pesi}>{Capacity} (ossia supera la capacità dello zaino per questa domanda)."
            else:
                return evaluation_format("No", 0,pt_red,index_pt)+"A questa domanda è richiesto si risponda con una lista di oggetti (esempio ['B','D'])."    
    
    
    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport'],
                     "trusted": True}
    plib.add_cell(notebook, cell_type="Code", data=cell_string, metadata=cell_metadata)

    # Description 1
    cell_string=f"Si consideri uno zaino di capienza $CapacityMax$ = {'CapacityMax'} e i seguenti oggetti {elementi}, aventi i seguenti pesi {pesi} e valori {valori}."
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": [],
                     "trusted": True}
    plib.add_cell(notebook,cell_type='Markdown', data=cell_string, metadata=cell_metadata)
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
