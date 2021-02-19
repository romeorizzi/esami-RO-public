from collections import OrderedDict
import nbformat as nb
import re
import os
import numpy as np
import re, ast
from sys import argv, exit, stderr
import yaml

PATH_UTILS = os.getcwd() + '/utils/'

def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())

def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)

setup_yaml()

def add_cell(note, cell_type,cell_string,cell_metadata):
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
    note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags":["noexport"]}

def insert_heading(note, exer_title):
    """It inserts the header and the exercise title
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt = open(PATH_UTILS + 'heading.md', 'r', encoding='utf-8').read()
    content_title = txt.replace('?title?', exer_title)
    note['cells'] += [nb.v4.new_markdown_cell(content_title)]
    note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": []}
    #note['cells'] += [nb.v4.new_markdown_cell('<b>NOTA</b>: qui sotto sono riportate alcune celle di codice con import necessari al funzionamento dei verificatori; ignorali pure. Clicca su "Avvio esercizio" e poi vai pure oltre la barra nera, per svolgere le richieste.')]
    #note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ["noexport"]}

def insert_n_tasks(note, n_tasks):
    text_n_tasks = """\
    n_tasks = """ + str(n_tasks) + """;
    arr_point= [-1] * n_tasks;"""
    note['cells'] += [nb.v4.new_code_cell(text_n_tasks)]
    note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "tags":["noexport"]}

# def insert_separator_bar(note):
#     content = '<h1>_______________________________________________________________________________________ </h1>'
#     note['cells'] += [nb.v4.new_markdown_cell(content)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ["noexport"]}
#     return

def insert_user_bar_lib(note):#, path_ex_folder):
    """It inserts the Python code to add the user bar needed to answer to each task
    Parameters:
    note (Jupyter nb.v4): the notebook
    path_ex_folder (str): the path of the current exercise where the mode has to be added"""
    user_bar_lib = open(PATH_UTILS + 'user_bar.py', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(user_bar_lib)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
    return

def insert_user_bar_cell(note):
    """It inserts the user bar as a code cell
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    user_bar_call = open(PATH_UTILS + 'user_bar_call.md').read()
    note['cells'] += [nb.v4.new_code_cell(user_bar_call)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
    return

def usage():
    print(f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml> è il nome del file coi dati di istanza specifica.""", file=stderr)

    
def generate_nb(path_yaml):
   # Notebook creation
    note = nb.v4.new_notebook()
    note['cells'] = []
    
    # Reading the instance
    exer = read_exercise_yaml(path_yaml)
    B=exer['B']
    elementi=exer['elementi']
    pesi=exer['pesi']
    valori=exer['valori']
    
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
    yaml_gen['tags']=exer['tags']
    tasks_istanza_libera=[]

    instance=B
    
    # Heading and needed import
    insert_user_bar_lib(note)
    insert_heading(note, exer['title']) # heading with title
    insert_import_mode_free(note)
    insert_n_tasks(note, n_tasks)
    
    # Knapsack
    cell_type='Code'
    cell_string=f"""\
    B= {B}
    elementi= {elementi}
    pesi = {pesi}
    valori = {valori}
    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ["noexport"], "trusted": True}
    add_cell(note, cell_type,cell_string,cell_metadata)

    # Verifier
    cell_type="Code"
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
    
    def verifknapsack(elementi,pesi, valori, MAX_CAP,answer,pt_green,pt_red, index_pt,edr=False):
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
        S = [[0 for j in range(MAX_CAP+1)] for i in range(n)] 
        for i in range(1,n):
            for j in range(MAX_CAP+1):
                S[i][j] = S[i-1][j]
                if pesi2[i] <= j and S[i-1][j-pesi2[i]] + valori2[i] > S[i][j]:
                    S[i][j] = S[i-1][j-pesi2[i]] + valori2[i]
        max_val=S[-1][-1]
        if type(answer)==int:
            if answer==max_val:
                return evaluation_format("Si", 1,pt_red,index_pt)+"La somma massima dei valori è ammissibile."
            else:
                return evaluation_format("Si", 1,pt_red,index_pt)+"La somma massima dei valori è ammissibile."
        if type(answer)==list:
            sum=0
            for i in range(len(answer)):
                sum+=valori2[elementi.index(answer[i])]
            if sum==max_val:
                return evaluation_format("Si", 1,pt_red,index_pt)+"Il sottoinsieme di elementi è ammissibile."
            else:
                return evaluation_format("Si", 1,pt_red,index_pt)+"Il sottoinsieme di elementi è ammissibile."
        else:
            return evaluation_format("No", 0,pt_red,index_pt)+"La risposta non è nel forma giusta."
    
    
    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ["noexport"],
                     "trusted": True}
    add_cell(note, cell_type, cell_string, cell_metadata)

    # Description 1
    cell_type='Markdown'
    cell_string=f"Si consideri uno zaino di capienza $B$ = {B} e i seguenti oggetti {elementi}, aventi i seguenti pesi {pesi} e valori {valori}."
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": [],
                     "trusted": True}
    add_cell(note,cell_type, cell_string, cell_metadata)
    yaml_gen['description1'] = cell_string
    
    # Requests
    for i in range (0,len(tasks)):
    
        if tasks[i]['request']=="R1":
            request=f"__Richiesta {i} [{tasks[i]['tot_points']} punti]__: Fornire la somma massima dei valori degli elementi ottenibile selezionando un sottoinsieme di elementi tali che la somma dei loro pesi non ecceda $B$."
            verif=f"display(Markdown(verifknapsack(elementi,pesi,valori,B,answer{num_of_question - 1}, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1})))"
        elif tasks[i]['request']=="R2":
            request=f"__Richiesta {i} [{tasks[i]['tot_points']} punti]__: Fornire un sottoinsieme di elementi tale che la somma dei valori corrispondenti sia la massima possibile e che la somma dei loro pesi non ecceda $B$."
            verif=f"display(Markdown(verifknapsack(elementi,pesi,valori,B,answer{num_of_question - 1}, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1})))"
        elif tasks[i]['request'] == "R3":
            request=f"__Richiesta {i} [{tasks[i]['tot_points']} punti]__: Fornire la somma massima dei valori degli elementi ottenibile <b>se non si considerano i seguenti elementi {tasks[i]['edr']}</b>."
            verif=f"display(Markdown(verifknapsack(elementi,pesi,valori,B,answer{num_of_question - 1}, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1},edr={tasks[i]['edr']})))"
        elif tasks[i]['request'] == "R4":
            request=f"__Richiesta {i} [{tasks[i]['tot_points']} punti]__: Fornire la somma massima dei valori degli elementi <b> se __B__ diventa {tasks[i]['B2']}</b>."
            verif=f"display(Markdown(verifknapsack(elementi,pesi,valori,{tasks[i]['B2']},answer{num_of_question - 1}, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1})))"
        else:
            assert False
            
        # Single request text
        cell_type='Markdown'
        cell_string=request
        cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
        add_cell(note, cell_type, cell_string, cell_metadata)
        tasks_istanza_libera+=[{'tot_points' : tasks[i]['tot_points'],'ver_points': tasks[i]['ver_points'], 'description1':request}]

        # Single request answer
        if tasks[i]['request'] == "R2":
            cell_type='Code'
            cell_string=f'#Inserisci la risposta (in forma di lista)\nanswer{num_of_question - 1}=[]'
            cell_metadata={"init_cell": True, "trusted": True, "deletable": False}
            add_cell(note,cell_type,cell_string,cell_metadata)
    
        else:
            cell_type='Code'
            cell_string=f'#Inserisci la risposta (numero)\nanswer{num_of_question - 1}=-1'
            cell_metadata={"init_cell": True, "trusted": True, "deletable": False}
            add_cell(note,cell_type,cell_string,cell_metadata)
        
        # Single request verifier
        cell_type='Code'
        cell_string=verif
        cell_metadata={"init_cell": True, "hide_input": True, "editable": False, "deletable": False, "trusted": True}
        add_cell(note,cell_type,cell_string,cell_metadata)
        num_of_question += 1
    
    
    yaml_gen['tasks']=tasks_istanza_libera
    return note, yaml_gen

