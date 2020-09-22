#!/usr/bin/python3

from collections import OrderedDict
import nbformat as nb
import re
import os
from sys import argv, exit, stderr
import yaml

PATH_UTILS = os.getcwd() + '/utils/'

def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())

def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)

setup_yaml()

def add_cell(note,cell_type,cell_string,cell_metadata):
    if cell_type=="Code":
        note['cells'].append(nb.v4.new_code_cell(cell_string,metadata=cell_metadata));
    elif cell_type=="Markdown":
        note['cells'].append(nb.v4.new_markdown_cell(cell_string,metadata=cell_metadata));
    elif cell_type=="Raw":
        note['cells'].append(nb.v4.new_raw_cell(cell_string,metadata=cell_metadata));
    else:
        assert False

def read_exercise_yaml(path_yaml):
    """It reads a yaml file and save its content in a dictionary
    Parameters:
    path_yaml (str): the path to the yaml instance"""
    exer_dict = {}
    with open(path_yaml, 'r') as stream:
        try:
            exer_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return exer_dict

def insert_import_mode_free(note):
    """It imports the proper modules and libraries needed for all notebooks
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt_import = open(PATH_UTILS + 'import_mode_free.md', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(txt_import)]
    note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags":['run_start','noexport']}

def insert_heading(note, exer_title):
    """It inserts the header and the exercise title
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt = open(PATH_UTILS + 'heading.md', 'r', encoding='utf-8').read()
    content_title = txt.replace('?title?', exer_title)
    note['cells'] += [nb.v4.new_markdown_cell(content_title)]
    note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start']}
    #note['cells'] += [nb.v4.new_markdown_cell('<b>NOTA</b>: qui sotto sono riportate alcune celle di codice con import necessari al funzionamento dei verificatori; ignorali pure. Clicca su "Avvio esercizio" e poi vai pure oltre la barra nera, per svolgere le richieste.')]
    #note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
    
def insert_n_tasks(note, n_tasks):
    text_import = """\
    from tabulate import tabulate
    import copy
    n_tasks = """ + str(n_tasks) + """;
    arr_point = [-1] * n_tasks;"""
    note['cells'] += [nb.v4.new_code_cell(text_import)]
    note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags":['run_start','noexport']}

# def insert_separator_bar(note):
#     content = '<h1>_______________________________________________________________________________________ </h1>'
#     note['cells'] += [nb.v4.new_markdown_cell(content)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
#     return 

# def insert_user_bar_lib(note):#, path_ex_folder):
#     """It inserts the Python code to add the user bar needed to answer to each task
#     Parameters:
#     note (Jupyter nb.v4): the notebook
#     path_ex_folder (str): the path of the current exercise where the mode has to be added"""
#     user_bar_lib = open(PATH_UTILS + 'user_bar.py', 'r', encoding='utf-8').read()
#     note['cells'] += [nb.v4.new_code_cell(user_bar_lib)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
#     return

# def insert_user_bar_cell(note):
#     """It inserts the user bar as a code cell
#     Parameters:
#     note (Jupyter nb.v4): the notebook"""
#     user_bar_call = open(PATH_UTILS + 'user_bar_call.md').read()
#     note['cells'] += [nb.v4.new_code_cell(user_bar_call)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
#     return

def generate_nb(path_yaml):
    # Notebook creation
    note = nb.v4.new_notebook()
    note['cells'] = []
    
    # Reading the instance
    exer = read_exercise_yaml(path_yaml)
    campo_minato=exer['campo_minato']
    tasks=exer['tasks']
    total_point=0
    n_tasks = 0
    for i in range (0,len(tasks)):
            total_point+=tasks[i]['tot_points']
            n_tasks += 1
    num_of_question=1
    
    yaml_gen=OrderedDict()
    yaml_gen['name']=exer['name']
    yaml_gen['title']=exer['title']
    tasks_istanza_libera=[]

    m=len(exer['campo_minato'])
    n=len(exer['campo_minato'][0])
    
    # Heading and needed import
    insert_heading(note, exer['title']) # heading with title
    insert_import_mode_free(note)
    insert_n_tasks(note, n_tasks)

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
    instance=f"campo_minato={exer['campo_minato']}"
    cell_type='Code'
    cell_string = f"""
    campo_minato = {exer['campo_minato']}
    m = len(campo_minato)
    n = len(campo_minato[0])
    mappa = [ ["*"]*(n+1) ] + [ (["*"] + r) for r in campo_minato]
    """
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ["noexport"], "trusted": True}
    add_cell(note,cell_type,cell_string,cell_metadata)
   
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
        display(Markdown(f"La tua versione attuale della matrice ${Latex_type(nome_matrice)}$ è la seguente:"))
        visualizza(matrice)
        display(Markdown(f"<b>Validazione della tua matrice ${Latex_type(nome_matrice)}$:</b>"))
        display(Markdown(eval(f"check_{nome_matrice}(mappa,matrice,pt_green, pt_red, index_pt)")))
    """
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ["noexport"], "trusted": True}
    add_cell(note,cell_type,cell_string,cell_metadata)
    
    # Useful note
    cell_type='Markdown'
    cell_string="""<b>Nota</b>: Saper programmare non è la competenza che intendiamo valutare con questo esercizio.
    Decidi tu, in piena libertà, se preferisci compilare le tabelle e le risposte a mano, oppure scrivere del codice che lo faccia per te
    o che ti assista nelle misura che ti è più utile. Sei incoraggiato a ricercare l'approccio per te più pratico, sicuro e conveniente.
    Non verranno pertanto attribuiti punti extra per chi scrive del codice. I punti ottenuti dalle risposte consegnate a chiusura sono l'unico elemento oggetto di valutazione.
    In ogni caso, il feedback offerto dalle procedure di validazione rese disponibili è di grande aiuto.
    Esso convalida la conformità delle tue risposte facendo anche presente a quanti dei punti previsti  le tue risposte possono ambire.
    Per facilitare chi di voi volesse scrivere del codice a proprio supporto, abbiamo aggiunto alla mappa di $m$ righe ed $n$ colonne una riga e colonna iniziale (di indice zero), fatte interamente di mine, perchè non si crei confusione col fatto che gli indici di liste e array in programmazione partono da zero.
    """
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ["noexport"], "trusted": True}
    add_cell(note,cell_type,cell_string,cell_metadata)

    # Description1
    cell_type='Markdown'
    cell_string=f"Un robot, inizialmente situato nella cella ${chr(65)}{1}={(1,1)}$, deve portarsi nella cella "\
           +f"${chr(64+m)}{n}=({m},{n})$." \
           +f"Le celle che riportano il simbolo '*' contengono una mina od altre trapole mortali, ed il robot deve evitarle." \
           +f"I movimenti base possibili sono il passo verso destra (ad esempio il primo passo potrebbe avvenire dalla cella $A1$ alla cella $A2$)" \
           + f" ed il passo verso il basso (ad esempio, come unica altra alternativa per il primo passo il robot "\
           + f"potrebbe portarsi quindi nella cella $B1$)."\
           + f"Quanti sono i possibili percorsi che può fare il robot per andare dalla cella ${chr(65)}{1}={(1,1)}$ alla cella ${chr(64+m)}{n}=({m},{n})$?"
    cell_metadata = {"init_cell": True, "hide_input": True, "editable": False, "deletable": False, "tags": [], "trusted": True}
    add_cell(note,cell_type,cell_string,cell_metadata)

    # Description2
    cell_type='Code'
    cell_string="""visualizza(mappa)"""
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ["noexport"], "trusted": True}
    add_cell(note,cell_type,cell_string,cell_metadata)

    # Requests
    for i in range (0,len(tasks)):
        verif=""
        if tasks[i]['request']=="R1":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: A mano o tramite un programma componi la matrice $num\_paths\_to$ di dimensione $(m+1)\\times(n+1)$ e tale per cui in $num\_paths\_to[i][j]$ sia riposto il numero di cammini dalla cella $A1=(1,1)$ alla generica cella $(i,j)$, per ogni $i = 0,..., m+1$ e $j = 0,..., n+1$."
            request_lib = f"A mano o tramite un programma componi la matrice num_paths_to di dimensione " + str(m+1) + " x " + str(n+1) + " e tale per cui in num_paths_to[i][j] sia riposto il numero di cammini dalla cella A1=(1,1) alla generica cella (i,j), per ogni i = 0, ..., m+1 e j = 0, ..., n+1"
            answer_type = "Code"
            answer=num_paths_to
            verif=f"visualizza_e_valuta('num_paths_to',num_paths_to, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})"
        elif tasks[i]['request'] =="R2":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Componi ora una matrice $num\_paths\_from$ di dimensione $(m+2)\\times(n+2)$" \
                        +f" e tale per cui in $num\_paths\_from[i][j]$, per ogni $i = 1,..., m+1$ e $j = 1,..., n+1$," \
                        +f" sia riposto il numero di cammini dalla generica cella $(i,j)$ alla cella "\
                        +f"${chr(64+m)}{n}=({m},{n})$."
            request_lib = f"Componi ora una matrice num_paths_from di dimensione " + str(m+2) + " x " + str(n+2) + " e tale per cui in num_paths_from[i][j] sia riposto il numero di cammini dalla generica cella (i,j) alla cella " + str(chr(64+m)) + str(n) + "=("+str(m) + "," + str(n) + "), per ogni i = 0, ..., m+1 e j = 0, ..., n+1"
            answer_type="Code"
            answer=num_paths_from
            verif= f"visualizza_e_valuta('num_paths_from',num_paths_from, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})"
        elif tasks[i]['request'] == "R3":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Quanti sono i percorsi con partenza in $A1=(1,1)$ e arrivo in ${chr(64+m)}{n}=({m},{n})$."
            request_lib = f"Quanti sono i percorsi con partenza in A1(1,1) e arrivo in " + str(chr(64+m)) + str(n) + "=(" + str(m) + "," + str(n) + ")?"
            answer_type="Markdown"
            answer="Inserisci la risposta"
        elif tasks[i]['request'] =="R4":
            start_point=eval(tasks[i]['start_point'])
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Quanti sono i percorsi con partenza in ${chr(64+start_point[0])}{start_point[1]}={start_point}$ e arrivo in ${chr(64+m)}{n}=({m},{n})$."
            request_lib=f"Quanti sono i percorsi con partenza in " + str(chr(64+start_point[0])) + str(start_point[1]) + "="+ str(start_point) + " e arrivo in " + str(chr(64+m)) + str(n) + "= (" + str(m) + "," + str(n) + ")?"
            answer_type = "Markdown"
            answer = "Inserisci la risposta"
        elif tasks[i]['request'] =="R5":
            target_point=eval(tasks[i]['target_point'])
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Quanti sono i percorsi con partenza in $A1=(1,1)$ e arrivo in ${chr(64+target_point[0])}{target_point[1]}={target_point}$?"
            request_lib=f"Quanti sono i percorsi con partenza in A1=(1,1) e arrivo in " + str(chr(64+target_point[0]))+str(target_point[1]) + "=" + str(target_point) + "?"
            answer_type = "Markdown"
            answer = "Inserisci la risposta"
        elif tasks[i]['request'] =="R6":
            middle_point=eval(tasks[i]['middle_point'])
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Quanti sono i percorsi che partono da $A1=(1,1)$, passano da ${chr(64+middle_point[0])}{middle_point[1]}={middle_point}$, e arrivano in ${chr(64+m)}{n}=({m},{n})$?"
            request_lib = f"Quanti sono i percorsi che partono da A1=(1,1), passano da " + str(chr(64+middle_point[0])) + str(middle_point[1]) + "=" + str(middle_point) + " e arrivano in " + str(chr(64+m)) + str(n) + "=(" + str(m) + "," + str(n) + ")?" 
            answer_type = "Markdown"
            answer = "Inserisci la risposta"

        # aggiungere altre possibili richieste e relativi verificatori
        else:
            assert False
        
        # Single request text
        cell_type='Markdown'
        cell_string= request
        cell_metadata ={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ["noexport"], "trusted": True}
        add_cell(note,cell_type,cell_string,cell_metadata)
        tasks_istanza_libera+=[{'tot_points' : tasks[i]['tot_points'],'ver_points': tasks[i]['ver_points'], 'description1':request_lib}]
        
        # Single request answer
        cell_type=answer_type
        cell_string=answer
        cell_metadata={"init_cell": True, "trusted": True, "deletable": False}
        add_cell(note,cell_type,cell_string,cell_metadata)

        # Single request verifier
        if verif !="":
            cell_type='Code'
            cell_string=verif
            cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "trusted": True}
            add_cell(note,cell_type,cell_string,cell_metadata)
    
        num_of_question += 1
    
    yaml_gen['tasks']=tasks_istanza_libera
    return note, yaml_gen
