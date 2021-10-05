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
from tabulate import tabulate

import problems_common_lib as plib

PATH_UTILS = os.getcwd() + '/utils/'

def read_str_as_pair_of_ints(pair_str):
    x,y=pair_str[1:-1].split(',')
    return (int(x),int(y))

def generate_nb(fullpath_yaml):
    # Notebook creation
    notebook = nb.v4.new_notebook()
    notebook['cells'] = []

    # Reading the instance
    exer = plib.read_exercise_yaml(fullpath_yaml)
    campo_minato=exer['instance']['campo_minato']
#    start_point=read_str_as_pair_of_ints(exer['instance']['start_point'])
#    target_point=read_str_as_pair_of_ints(exer['instance']['target_point'])
#    middle_point=read_str_as_pair_of_ints(exer['instance']['middle_point'])
    
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

    m=len(campo_minato)
    n=len(campo_minato[0])
    mappa = [ ["*"]*(n+1) ] + [ (["*"] + r) for r in campo_minato]
    if len(mappa)==m+1 and len(mappa[0])==n+1:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:] for r in mappa[1:]]


    if len(mappa)==m+2 and len(mappa[0])==n+2:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:-1] for r in mappa[1:-1]]

    columns=[str(i) for i in range(1,n+1)]
    v_mappa=tabulate(aux, headers=columns, tablefmt='fancy_grid', showindex=index)

    # Heading and needed import
    plib.insert_user_bar_lib(notebook, run_cells=True)
    plib.insert_heading(notebook, exer['title'], run_cells=True) # heading with title
    plib.insert_import_mode_free(notebook, run_cells=True)
    plib.insert_n_tasks(notebook, n_tasks, run_cells=True)

    # BEGIN dynamic programming table input in the notebook
    # First DP table:
    num_paths_to=f"num_paths_to=["
    for i in range (m+1):
        num_paths_to=num_paths_to+"\n\t\t"+str([0]*(n+1))+","
        if i > 0:
            num_paths_to += "\t\t# " + str(campo_minato[i-1])
    num_paths_to = num_paths_to + "\n]"

    # Second DP table:
    num_paths_from=f"num_paths_from=["
    for i in range (m+2):
        num_paths_from=num_paths_from+"\n\t\t"+str([0]*(n+2))+","
        if i > 0 and i <= m:
            num_paths_from += "\t\t# " + str(campo_minato[i-1])
    num_paths_from = num_paths_from + "\n]"
    # END dynamic programming table input in the notebook

    # Adding campo_minato and mappa in the notebook"
    cell_type='Code'
    cell_string = f"""
    campo_minato = {campo_minato}
    m = len(campo_minato)
    n = len(campo_minato[0])
    num_paths_to={num_paths_to}
    num_paths_from={num_paths_from}
    mappa = [ ["*"]*(n+1) ] + [ (["*"] + r) for r in campo_minato]
    """
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ['noexport'], "trusted": True}
    plib.add_cell(notebook,cell_type,data=cell_string,metadata=cell_metadata)

    # Verifier
    cell_type="Code"
    cell_string= """\
    def visualizza(env):
        if len(env)==m+1 and len(env[0])==n+1:
            index=[chr(65+i) for i in range(m)]
            aux=[r[1:] for r in env[1:]]


        if len(env)==m+2 and len(env[0])==n+2:
            index=[chr(65+i) for i in range(m)]
            aux=[r[1:-1] for r in env[1:-1]]

        columns=[str(i) for i in range(1,n+1)]
        print(tabulate(aux, headers=columns, tablefmt='fancy_grid', showindex=index))


    def evaluation_format(answ, pt_green,pt_red, index_pt):
        pt_blue=0
        if pt_green!=0:
            if answ == "Si":
                pt_green=pt_red
                pt_red=0
                pt_blue=pt_green
            else:
                pt_blue=pt_red-pt_green
                pt_red=0
        arr_point[index_pt]=pt_green
        file = open("points.txt", "w")
        file.write(str(arr_point))
        file.close()
        return f"{answ}. Totalizzeresti <span style='color:green'>[{pt_green} safe pt]</span>, \
                                        <span style='color:blue'>[{pt_blue} possible pt]</span>, \
                                        <span style='color:red'>[{pt_red} out of reach pt]</span>.<br>"

    def check_num_paths_to(mappa, num_paths_to, pt_green, pt_red, index_pt, return_only_boolean=False):
        if len(num_paths_to) != m+1:
            if return_only_boolean:
                    return False
            return evaluation_format("No", 0, pt_red,index_pt)+f"Le righe della matrice $num\_paths\_to$ devono essere $m+1=${m+1}, non {len(num_paths_to)}."
        if len(num_paths_to[0]) != n+1:
            if return_only_boolean:
                    return False
            return evaluation_format("No", 0, pt_red, index_pt)+f"Le colonne della matrice $num\_paths\_to$ devono essere $n+1=${n+1}, non {len(num_paths_to[0])}."

        for i in range (0,m):
            if num_paths_to[i][0]!=0:
                if return_only_boolean:
                    return False
                return evaluation_format("No", 0, pt_red, index_pt)+f"Attenzione, i cammini devono partire dalla cella $(1,1)$ e pertanto $num\_paths\_to[${i}$][0] = 0$"
        for j in range (0,n):
            if num_paths_to[0][j]!=0:
                if return_only_boolean:
                    return False
                return evaluation_format("No", 0, pt_red, index_pt)+f"Attenzione, i cammini devono partire dalla cella $(1,1)$ e pertanto $num\_paths\_to[0][${j}$] = 0$"
        num_paths_to_forgiving = copy.deepcopy(num_paths_to)
        num_paths_to_forgiving[1][1] = 1
        for i in range(m,0,-1):
            for j in range (n,0,-1):
                if i==1 and j==1:
                    if return_only_boolean:
                        return True
                    return  evaluation_format("Si", pt_green, pt_red, index_pt)+"Non riscontro particolari problemi della tua versione della matrice $num\_paths\_to$."
                if mappa[i][j]!="*":
                    if num_paths_to_forgiving[i][j]!=num_paths_to_forgiving[i-1][j]+num_paths_to_forgiving[i][j-1]:
                        if return_only_boolean:
                            return False
                        return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_to$."
                elif num_paths_to_forgiving[i][j]!=0:
                    if return_only_boolean:
                        return False
                    return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_to$."


    def check_num_paths_from(mappa, num_paths_from, pt_green, pt_red, index_pt, return_only_boolean=False):
        if len(num_paths_from) != m+2:
            if return_only_boolean:
                return False
            return evaluation_format("No", 0, pt_red, index_pt)+f"Le righe della matrice $num\_paths\_from$ devono essere $m+2=${m+2}, non {len(num_paths_from)}."
        if len(num_paths_from[0]) != n+2:
            if return_only_boolean:
                    return False
            return evaluation_format("No", 0, pt_red, index_pt)+f"Le colonne della matrice $num\_paths\_from$ devono essere $n+2=${n+2}, non {len(num_paths_from[0])}."

        for i in range (0,m+1):
            if num_paths_from[i][n+1]!=0:
                if return_only_boolean:
                    return False
                return evaluation_format("No", 0, pt_red, index_pt)+f"Attenzione, i cammini devono partire dalla cella $(8,9)$ e pertanto $num\_paths\_from[${i}$][10] = 0$"
        for j in range (0,n+1):
            if num_paths_from[m+1][j]!=0:
                if return_only_boolean:
                    return False
                return evaluation_format("No", 0, pt_red, index_pt)+f"Attenzione, i cammini devono partire dalla cella $(8,9)$ e pertanto $num\_paths\_from[9][${j}$] = 0$"
        num_paths_from_forgiving = copy.deepcopy(num_paths_from)
        num_paths_from_forgiving[m][n] = 1
        for i in range(1,m-1):
            for j in range (1,n-1):
                if mappa[i][j]!="*":
                    if num_paths_from_forgiving[i][j]!=num_paths_from_forgiving[i+1][j]+num_paths_from_forgiving[i][j+1]:
                        if return_only_boolean:
                            return False
                        return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
                elif num_paths_from_forgiving[i][j]!=0:
                    if return_only_boolean:
                        return False
                    return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
        for i in range (1, m):
            if mappa[i][n]!="*":
                if num_paths_from_forgiving[i][n]!=num_paths_from_forgiving[i+1][n]+num_paths_from_forgiving[i][n+1]:
                    if return_only_boolean:
                        return False
                    return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
            elif num_paths_from_forgiving[i][n]!=0:
                if return_only_boolean:
                    return False
                return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
        for j in range (1, n):
            if mappa[m][j]!="*":
                if num_paths_from_forgiving[m][j]!=num_paths_from_forgiving[m+1][j]+num_paths_from_forgiving[m][j+1]:
                    if return_only_boolean:
                        return False
                    return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
            elif num_paths_from_forgiving[m][j]!=0:
                if return_only_boolean:
                    return False
                return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
        if return_only_boolean:
            return True
        return  evaluation_format("Si", pt_green, pt_red, index_pt)+"Non riscontro particolari problemi della tua versione della matrice $num\_paths\_from$."

    def Latex_type(string):
        return string.replace("_", "\_")

    def visualizza_e_valuta(nome_matrice, matrice, pt_green, pt_red, index_pt):
        display(Markdown(f"La tua versione attuale della matrice ${Latex_type(nome_matrice)}$  la seguente:"))
        visualizza(matrice)
        display(Markdown(f"<b>Validazione della tua matrice ${Latex_type(nome_matrice)}$:</b>"))
        display(Markdown(eval(f"check_{nome_matrice}(mappa,matrice,pt_green, pt_red, index_pt)")))
    """
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ['noexport'], "trusted": True}
    plib.add_cell(notebook,cell_type,data=cell_string,metadata=cell_metadata)

    # Useful notebook
    cell_type='Markdown'
    cell_string="""<b>Nota</b>: Saper programmare non  la competenza che intendiamo valutare con questo esercizio.
    Decidi tu, in piena libert, se preferisci compilare le tabelle e le risposte a mano, oppure scrivere del codice che lo faccia per te
    o che ti assista nelle misura che ti  pi utile. Sei incoraggiato a ricercare l'approccio per te pi pratico, sicuro e conveniente.
    Non verranno pertanto attribuiti punti extra per chi scrive del codice. I punti ottenuti dalle risposte consegnate a chiusura sono l'unico elemento oggetto di valutazione.
    In ogni caso, il feedback offerto dalle procedure di validazione rese disponibili  di grande aiuto.
    Esso convalida la conformit delle tue risposte facendo anche presente a quanti dei punti previsti  le tue risposte possono ambire.
    Per facilitare chi di voi volesse scrivere del codice a proprio supporto, abbiamo aggiunto alla mappa di $m$ righe ed $n$ colonne una riga e colonna iniziale (di indice zero), fatte interamente di mine, perch non si crei confusione col fatto che gli indici di liste e array in programmazione partono da zero.
    """
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ['noexport'], "trusted": True}
    plib.add_cell(notebook,cell_type,data=cell_string,metadata=cell_metadata)

    # Description1
    cell_type='Markdown'
    cell_string=f"Un robot, inizialmente situato nella cella ${chr(65)}{1}={(1,1)}$, deve portarsi nella cella "\
           +f"${chr(64+m)}{n}=({m},{n})$." \
           +f"Le celle che riportano il simbolo '*' contengono una mina od altre trapole mortali, ed il robot deve evitarle." \
           +f"I movimenti base possibili sono il passo verso destra (ad esempio il primo passo potrebbe avvenire dalla cella $A1$ alla cella $A2$)" \
           + f" ed il passo verso il basso (ad esempio, come unica altra alternativa per il primo passo il robot "\
           + f"potrebbe portarsi quindi nella cella $B1$)."\
           + f"Quanti sono i possibili percorsi che pu fare il robot per andare dalla cella ${chr(65)}{1}={(1,1)}$ alla cella ${chr(64+m)}{n}=({m},{n})$?"
    cell_metadata = {"init_cell": True, "hide_input": True, "editable": False, "deletable": False, "tags": [], "trusted": True}
    plib.add_cell(notebook,cell_type,data=cell_string,metadata=cell_metadata)
    yaml_gen['description1'] = cell_string

    # Description3
    cell_type='Code'
    cell_string=f"""
    from tabulate import tabulate
    print(tabulate({aux}, headers={columns}, tablefmt="fancy_grid", showindex={index}))"""
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ['noexport'], "trusted": True}
    plib.add_cell(notebook,cell_type,data=cell_string,metadata=cell_metadata)
    yaml_gen['description3'] = cell_string


    # Requests
    for i in range(len(tasks)):
        task=tasks[i][i+1]
        if 'start_point' in task.keys():
            start_point=read_str_as_pair_of_ints(task['start_point'])
        if 'target_point' in task.keys():
            target_point=read_str_as_pair_of_ints(task['target_point'])
        if 'middle_point' in task.keys():
            middle_point=read_str_as_pair_of_ints(task['middle_point'])
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
        # cell_metadata ={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ['noexport'], "trusted": True}

        # Single request answer cell:
        # cell_metadata={"init_cell": True, "trusted": True, "deletable": False}

        # Single request verifier cell:
        # cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "trusted": True}

