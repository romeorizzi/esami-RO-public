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

def add_cell(note,cell_type, cell_string, cell_metadata):
    if cell_type == "Code":
        note['cells'].append(nb.v4.new_code_cell(cell_string, metadata=cell_metadata))
    elif cell_type == "Markdown":
        note['cells'].append(nb.v4.new_markdown_cell(cell_string, metadata=cell_metadata))
    elif cell_type == "Raw":
        note['cells'].append(nb.v4.new_raw_cell(cell_string, metadata=cell_metadata))
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
    note.cells[-1].metadata = {"hide_input": True, "trusted":True, "init_cell": True, "editable": False, "deletable": False, "tags":['run_start','noexport']}

def insert_heading(note, exer_title):
    """It inserts the header and the exercise title
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt = open(PATH_UTILS + 'heading.md', 'r', encoding='utf-8').read()
    content_title = txt.replace('?title?', exer_title)
    note['cells'] += [nb.v4.new_markdown_cell(content_title)]
    note.cells[-1].metadata = {"hide_input": True, "trusted":True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start']}
    #note['cells'] += [nb.v4.new_markdown_cell('<b>NOTA</b>: qui sotto sono riportate alcune celle di codice con import necessari al funzionamento dei verificatori; ignorali pure. Clicca su "Avvio esercizio" e poi vai pure oltre la barra nera, per svolgere le richieste.')]
    #note.cells[-1].metadata = {"hide_input": True, "trusted":True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
    
def insert_n_tasks(note, n_tasks):    
    text_n_tasks = """\
    n_tasks = """ + str(n_tasks) + """;
    arr_point = [-1] * n_tasks;"""
    note['cells'] += [nb.v4.new_code_cell(text_n_tasks)]
    note.cells[-1].metadata = {"hide_input": True, "trusted":True, "init_cell": True, "editable": False, "deletable": False, "tags":['run_start','noexport']}

# def insert_separator_bar(note):
#     content = '<h1>_______________________________________________________________________________________ </h1>'
#     note['cells'] += [nb.v4.new_markdown_cell(content)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted":True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
#     return 

# def insert_user_bar_lib(note):#, path_ex_folder):
#     """It inserts the Python code to add the user bar needed to answer to each task
#     Parameters:
#     note (Jupyter nb.v4): the notebook
#     path_ex_folder (str): the path of the current exercise where the mode has to be added"""
#     user_bar_lib = open(PATH_UTILS + 'user_bar.py', 'r', encoding='utf-8').read()
# note['cells'] += [nb.v4.new_code_cell(user_bar_lib)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted":True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
#     return

# def insert_user_bar_cell(note):
#     """It inserts the user bar as a code cell
#     Parameters:
#     note (Jupyter nb.v4): the notebook"""
#     user_bar_call = open(PATH_UTILS + 'user_bar_call.md').read()
#     note['cells'] += [nb.v4.new_code_cell(user_bar_call)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted":True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
#     return

def generate_nb(path_yaml):
    # Notebook creation
    note = nb.v4.new_notebook()
    note['cells'] = []
    
    # Reading the instance
    exer = read_exercise_yaml(path_yaml)
    s = exer['s']
    t = exer['t']
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

    instance = s
    instance1 = t

    # Heading and needed import
    insert_heading(note, exer['title']) # heading with title
    insert_import_mode_free(note)
    insert_n_tasks(note, n_tasks)
    
    # Adding s and t in the notebook
    cell_type = 'Code'
    cell_string = f"""\
    s = "{s}"
    t = "{t}"
    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ["noexport"],
                     "trusted": True}
    add_cell(note,cell_type, cell_string, cell_metadata)

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

    def verifLCS(string1, string2, answer, pt_green, pt_red, index_pt, start=False, end=False):
        if answer=="":
            return evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita è vuota."
        if start != False and answer[0]!=start:
            return evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita non inizia con __{start}__."
        if end != False and answer[len(answer)-1]!=end:
            return evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita non termina con __{end}__."
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
        if (is_sub(answer,string1)) and (is_sub(answer,string2)) and len(answer)==correct_len:
            return evaluation_format("Si", pt_green, pt_red, index_pt)+"La sottosequenza comune è corretta."
        elif (is_sub(answer,string1)) and (is_sub(answer,string2)) and len(answer)!=correct_len:
            return evaluation_format("No", 1, pt_red, index_pt)+"La sottosequenza comune non è massima."
        #if (is_sub(answer,string1)) and (is_sub(answer,string2)):
        #    return evaluation_format("Si", pt_green, pt_red, index_pt)+"La sottosequenza fornita è ammissibile."
        else:
            return evaluation_format("No", 0, pt_red, index_pt)+"La sottosequenza non è ammissibile."

    def evaluation_format(answ, pt_green, pt_red, index_pt):
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

    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ["noexport"],
                     "trusted": True}
    add_cell(note,cell_type, cell_string, cell_metadata)

    # Description1
    cell_type = 'Markdown'
    cell_string = "Si considerino le seguenti sequenze di caratteri:<br/><br/> $s$ = " + str(s) + "<br/>  $t$ = " + str(t)
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": [],
                     "trusted": True}
    add_cell(note,cell_type, cell_string, cell_metadata)
    yaml_gen['description1'] = cell_string
    
    # Requests
    for i in range (0,len(tasks)):

        if tasks[i]['request']=="R1":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Trovare la massima sottosequenza comune tra le <b> due stringhe</b>:<br/>$s$ = {s}<br/>$t$ = {t}."
            request_lib = f"Trovare la massima comune tra le due stringhe s = " + str(s) + " e t = " + str(t)
            verif=f"display(Markdown(verifLCS(s, t ,answer{num_of_question - 1},pt_green=1, pt_red={tasks[i]['tot_points']}, index_pt={num_of_question - 1})))"
        elif tasks[i]['request'] =="R2":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Trovare la massima sottosequenza comune utilizzando: <br/><b>il prefisso</b>  $t'$ = {tasks[i]['string_mod']} <br/>$s$ = {s}."
            request_lib = f"Trovare la massima sottosequenza comune utilizzando il prefisso t' = " + str(tasks[i]['string_mod']) + " e s = "+ str(s)
            verif= f"display(Markdown(verifLCS(s, '{tasks[i]['string_mod']}' ,answer{num_of_question - 1},pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"
        elif tasks[i]['request'] == "R3":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Trovare la massima sottosequenza comune utilizzando:<br/><b>il suffisso </b> $s'$ = {tasks[i]['string_mod']} <br/>$t$ = {t}."
            request_lib = f"Trovare la massima sottosequenza comune utilizzando il suffisso s' = " + str(tasks[i]['string_mod']) + " e t = " + str(t)
            verif=f"display(Markdown(verifLCS('{tasks[i]['string_mod']}', t ,answer{num_of_question - 1},pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"
        elif tasks[i]['request'] =="R4":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Trovare la massima sottosequenza comune tale che <b>inizi con la lettera </b> __{tasks[i]['start']}__ utilizzando:<br/>$s$ = {s}<br/>$t$ = {t}."
            request_lib = f"Trovare la massima sottosequenza comune tale che inizi con la lettera " + str(tasks[i]['start']) + " utilizzando s = " + str(s) + " e t = " + str(t)
            verif=f"display(Markdown(verifLCS('{tasks[i]['start']}'+s.split('{tasks[i]['start']}',1)[1], '{tasks[i]['start']}'+t.split('{tasks[i]['start']}',1)[1] ,answer{num_of_question - 1},pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1},start='{tasks[i]['start']}')))"
        elif tasks[i]['request'] =="R5":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Trovare la massima sottosequenza comune tale che <b>finisca con la lettera </b> __{tasks[i]['end']}__ utilizzando:<br/>$s$ = {s} <br/>$t$ = {t}."
            request_lib = f"Trovare la massima sottosequenza comune tale che finisca con la lettera " + str(tasks[i]['end']) + " utilizzando s = " + str(s) + " e t = " + str(t)
            verif=f"display(Markdown(verifLCS(s.rsplit('{tasks[i]['end']}',1)[0]+'{tasks[i]['end']}', t.rsplit('{tasks[i]['end']}',1)[0]+'{tasks[i]['end']}' ,answer{num_of_question - 1},pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1},end='{tasks[i]['end']}')))"
        else:
            assert False
        
        # Single request text
        cell_type='Markdown'
        cell_string= request
        cell_metadata ={"hide_input": True, "init_cell": True, "editable": False,  "deletable": False, "tags": [], "trusted": True}
        add_cell(note,cell_type,cell_string,cell_metadata)
        tasks_istanza_libera+=[{'tot_points' : tasks[i]['tot_points'],'ver_points': tasks[i]['ver_points'], 'description1':request_lib}]

        # Single request answer
        cell_type='Code'
        cell_string=f'#Inserisci la risposta\nanswer{num_of_question - 1}=""'
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
