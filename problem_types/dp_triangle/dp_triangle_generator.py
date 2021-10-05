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
import numpy as np
import ast

import problems_common_lib as plib

PATH_UTILS = os.getcwd() + '/utils/'


def usage():
    print(f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml>  il nome del file coi dati di istanza specifica.""", file=stderr)

def convert_to_LaTeX(triangolo):
    my_str=''
    line_str=''
    k=0
    my_str='%%latex'
    for i in range(0,len(triangolo)):
        for j in range(0,i+1):
            if j==0 or j==i:
                if j==0 and j==i:
                    line_str=line_str+str(f"$$ {triangolo[i,j]} $$")
                elif j==0 and j!=i:
                    line_str=line_str+str(f"$$ {triangolo[i,j]} \\qquad ")
                elif j!=0 and j==i:
                    line_str=line_str+str(f"{triangolo[i,j]} $$")
            if j<i and j!=0:
                line_str=line_str+str(f"{triangolo[i,j]} \\qquad ")
        my_str='\n'.join([my_str, line_str])
        line_str=''
    return my_str
    
def generate_nb(fullpath_yaml):
   # Notebook creation
    notebook = nb.v4.new_notebook()
    notebook['cells'] = []
    
    # Reading the instance
    exer = plib.read_exercise_yaml(fullpath_yaml)
    triangle_str=exer['instance']['triangle']
    # converto triangolo da stringa a numpy array
    triangle_mod = re.sub('\s+', '', str(triangle_str))
    triangle = np.array(ast.literal_eval(triangle_mod))
    
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
    
    m=len(triangle)
    vertex_sup=triangle[0,0]
    vertex_inf_sx=triangle[m-1,0]
    vertex_inf_dx=triangle[m-1,m-1]
    
    # Heading and needed import
    plib.insert_user_bar_lib(notebook, run_cells=False)
    plib.insert_heading(notebook, exer['title'], run_cells=False) # heading with title
    plib.insert_import_mode_free(notebook, run_cells=False)
    plib.insert_n_tasks(notebook, n_tasks, run_cells=False)
 
    # Triangle
    cell_string=f"""\
    triangle = {triangle_str}
    triangle=np.array(triangle)
    m={m}
    vertex_sup={vertex_sup}
    vertex_inf_sx={vertex_inf_sx}
    vertex_inf_dx={vertex_inf_dx}
    """  
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport'],
                     "trusted": True}
    plib.add_cell(notebook,cell_type='Code',data=cell_string,metadata=cell_metadata)
    
  # Verifier  
    cell_string= """\
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
    
    
    
    def is_path(path, triangle):  # verifichiamo che il percorso dato sia ammissibile per il triangolo di riferimento
        m=len(triangle)
        sol=True
        if (len(path)!=m) or (triangle[0,0]!=path[0]):
            sol=False
            return sol
        else:
            i=0
            j=0
            while i<(m-1) and j<(m-1):
                if (triangle[i+1,j]!=path[i+1]) and (triangle[i+1,j+1]!=path[i+1]):
                    sol=False
                    return sol
                else:
                    if (triangle[i+1,j]!=triangle[i+1,j+1]):
                        if (triangle[i+1,j]==path[i+1]):
                            i=i+1
                        else:   # (triangle[i+1,j+1]==path[i+1]):
                            i=i+1
                            j=j+1
                    else:
                        new_len=m-(i+1)
                        sol1=is_path(path[(i+1):m], triangle[(i+1):m, j:j+new_len])
                        sol2=is_path(path[(i+1):m], triangle[(i+1):m, (j+1):(j+1)+new_len])
                        if (sol1==False) and (sol2==False):
                            sol=False
                        elif (sol1==True) or (sol2==True):
                            sol=True
                        break   # l'istanza  risolta dalle precedenti chiamate ricorsive: si esce dal ciclo while
    
        return sol
    
    
    
    
    def verif_triangolo(answer, path, triangle, pt_green, pt_red, index_pt):
        if sum(path)!=answer:
            my_str="Errore: incongruenza tra il percorso e la somma forniti."
            if answer<np.max(triangle):
                str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita  inferiore al numero massimo presente nel triangolo, ovvero {np.max(triangle)}: se includi quest'ultimo hai gi una somma maggiore !"
            elif answer>np.sum(triangle):
                str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita  superiore alla somma di TUTTI i numeri presenti triangolo, ovvero {np.sum(triangle)}: certamente NON pu esistere un percorso del genere !"
            else:
                str_to_print=my_str
        else:
            if (is_path(path, triangle)): 
                str_to_print=evaluation_format("Si", pt_green, pt_red, index_pt) + "Il percorso  ammissibile."
            else:
                my_str="Il percorso non  ammissibile."
                if answer<np.max(triangle):
                    str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita  inferiore al numero massimo presente nel triangolo, ovvero {np.max(triangle)}: se includi quest'ultimo hai gi una somma maggiore !"
                elif answer>np.sum(triangle):
                    str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita  superiore alla somma di TUTTI i numeri presenti triangolo, ovvero {np.sum(triangle)}: certamente NON pu esistere un percorso del genere !"
                else:
                    str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str
        return str_to_print
    
    
    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport'],
                     "trusted": True}
    plib.add_cell(notebook, cell_type="Code", data=cell_string, metadata=cell_metadata)
    
    
    # Description 1
    cell_string=f"Nel seguente triangolo di numeri, con {vertex_sup} nel vertice superiore, {vertex_inf_sx} nel vertice inferiore sinistro, e {vertex_inf_dx} nel vertice inferiore destro.<br/>"
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False,
                     "trusted": True}
    plib.add_cell(notebook,cell_type='Markdown', data=cell_string, metadata=cell_metadata)
    yaml_gen['description1']=cell_string
    
    # Triangle in LaTeX
    cell_string=f"""\
    
    {convert_to_LaTeX(triangle)}
    
    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport'],
                     "trusted": True}
    plib.add_cell(notebook,cell_type='Code', data=cell_string, metadata=cell_metadata)
    yaml_gen['description3']=cell_string
    
    # Description 2
    cell_string ="\nSiamo interessati nei percorsi che partano dalla cima del triangolo e terminino da qualche parte sulla sua base. Ad ogni passo si può scendere di una riga, verticalmente oppure diagonalmente verso destra. Il **valore di un percorso**  la somma dei valori che visita."
    cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
    plib.add_cell(notebook,cell_type='Markdown',data=cell_string,metadata=cell_metadata)
    yaml_gen['description2']=cell_string

    
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
        # Single request text cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
       
        # Single request answer cell_metadata={"init_cell": True, "trusted": True, "deletable": False}
        
        # Single request verifier cell_metadata={"hide_input": False, "editable": False,  "deletable": False, "trusted": True, "tags": ['noexport']}
    
