"""
@authors:
Verifiers: Alessandro Busatto, Paolo Graziani, Aurora Rossi, Davide Roznowicz;
Integration: Alice Raffaele, Romeo Rizzi.

"""

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
    """ It adds a new cell (with the given type, text and metadata) to the notebook note 
    """
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

# def insert_user_bar_lib(note):#, path_ex_folder):
#     """It inserts the Python code to add the user bar needed to answer to each task
#     Parameters:
#     note (Jupyter nb.v4): the notebook
#     path_ex_folder (str): the path of the current exercise where the mode has to be added"""
#     user_bar_lib = open(PATH_UTILS + 'user_bar.py', 'r', encoding='utf-8').read()
#     note['cells'] += [nb.v4.new_code_cell(user_bar_lib)]
#     note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
#     return

# def insert_user_bar_cell(note):
#     """It inserts the user bar as a code cell
#     Parameters:
#     note (Jupyter nb.v4): the notebook"""
#     user_bar_call = open(PATH_UTILS + 'user_bar_call.md').read()
#     note['cells'] += [nb.v4.new_code_cell(user_bar_call)]
#     note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
#     return

def usage():
    print(f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml> è il nome del file coi dati di istanza specifica.""", file=stderr)

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
    
def generate_nb(path_yaml):
   # Notebook creation
    note = nb.v4.new_notebook()
    note['cells'] = []
    
    # Reading the instance
    exer = read_exercise_yaml(path_yaml)
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
    triangle_str=exer['triangle']

    # converto triangolo da stringa a numpy array
    triangle_mod = re.sub('\s+', '', str(triangle_str))
    triangle = np.array(ast.literal_eval(triangle_mod))
    
    m=len(triangle)
    vertex_sup=triangle[0,0]
    vertex_inf_sx=triangle[m-1,0]
    vertex_inf_dx=triangle[m-1,m-1]
    
    # Heading and needed import
    insert_user_bar_lib(note)
    insert_heading(note, exer['title']) # heading with title
    insert_import_mode_free(note)
    insert_n_tasks(note, n_tasks)
 
    # Triangle
    cell_type='Code'
    cell_string=f"""\
    triangle = {triangle_str}
    triangle=np.array(triangle)
    m={m}
    vertex_sup={vertex_sup}
    vertex_inf_sx={vertex_inf_sx}
    vertex_inf_dx={vertex_inf_dx}
    """  
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ["noexport"],
                     "trusted": True}
    add_cell(note,cell_type,cell_string,cell_metadata)
    
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
                        break   # l'istanza è risolta dalle precedenti chiamate ricorsive: si esce dal ciclo while
    
        return sol
    
    
    
    
    def verif_triangolo(answer, path, triangle, pt_green, pt_red, index_pt):
        if sum(path)!=answer:
            my_str="Errore: incongruenza tra il percorso e la somma forniti."
            if answer<np.max(triangolo):
                str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita è inferiore al numero massimo presente nel triangolo, ovvero {np.max(triangolo)}: se includi quest'ultimo hai già una somma maggiore !"
            elif answer>np.sum(triangolo):
                str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita è superiore alla somma di TUTTI i numeri presenti triangolo, ovvero {np.sum(triangolo)}: certamente NON può esistere un percorso del genere !"
            else:
                str_to_print=my_str
        else:
            if (is_path(path, triangle)): 
                str_to_print=evaluation_format("Si", pt_green, pt_red, index_pt) + "Il percorso è ammissibile."
            else:
                my_str="Il percorso non è ammissibile."
                if answer<np.max(triangolo):
                    str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita è inferiore al numero massimo presente nel triangolo, ovvero {np.max(triangolo)}: se includi quest'ultimo hai già una somma maggiore !"
                elif answer>np.sum(triangolo):
                    str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita è superiore alla somma di TUTTI i numeri presenti triangolo, ovvero {np.sum(triangolo)}: certamente NON può esistere un percorso del genere !"
                else:
                    str_to_print=evaluation_format("No", 0, pt_red, index_pt) + my_str
        return str_to_print
    
    
    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ["noexport"],
                     "trusted": True}
    add_cell(note, cell_type, cell_string, cell_metadata)
    
    
    # Description 1
    cell_type='Markdown'
    cell_string=f"Considerare il seguente triangolo di numeri, avente per vertice superiore {vertex_sup}, per vertice inferiore sinistro {vertex_inf_sx} e per vertice inferiore destro {vertex_inf_dx}.<br/>"
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False,
                     "trusted": True}
    add_cell(note,cell_type, cell_string, cell_metadata)
    
    # Triangle in LaTeX
    cell_type='Code'
    cell_string=f"""\
    
    {convert_to_LaTeX(triangle)}
    
    """
    cell_metadata = {"hide_input": True, "init_cell": True, "editable": False, "deletable": False, "tags": ["noexport"],
                     "trusted": True}
    add_cell(note,cell_type, cell_string, cell_metadata)
    
    # Description 2
    cell_type='Markdown'
    cell_string ="\nSiamo interessati ad analizzare i percorsi che partano dalla cima del triangolo e terminino da qualche parte sulla sua base. Ad ogni passo si può procedere o in basso o diagonalmente verso destra."
    cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
    add_cell(note,cell_type,cell_string,cell_metadata)
    yaml_gen['description2']=cell_string

    
    # Requests
    for i in range (0,len(tasks)):
        if tasks[i]['request'] =="R0":
            request=f"__Richiesta {i} [{tasks[i]['tot_points']} punti]__: Descrivere la sottostruttura ottima del problema."
            request_lib = f"Descrivere la sottostruttura ottima del problema."
            verif=f""
        elif tasks[i]['request']=="R1":
            request=f"__Richiesta {i} [{tasks[i]['tot_points']} punti]__: Calcolare la più grande somma di numeri ottenibile seguendo un percorso che parta dalla cima del triangolo e termini da qualche parte sulla sua base. Fornire, in qualità di certificato, il percorso sotto forma sequenza di numeri (array di interi) dalla cima alla base."
            verif=f"display(Markdown(verif_triangolo(somma, percorso, triangle, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1})))"
        elif tasks[i]['request']=="R2":
            request=f"__Richiesta {i} [{tasks[i]['tot_points']} punti]__: Provare a risolvere il problema in maniera ricorsiva considerando un'istanza di dimensione generica. Scrivere esplicitamente la ricorsione utilizzata, spiegando come si è arrivati a tale formulazione e qual è stato il ragionamento condotto. Abbozzare l'algoritmo che sfrutta tale ricorsione per risolvere il problema."
            verif=f""
        else:
            assert False
        
        # Single request text
        cell_type='Markdown'
        cell_string= request
        cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
        add_cell(note,cell_type,cell_string,cell_metadata)
        tasks_istanza_libera+=[{'tot_points' : tasks[i]['tot_points'],'ver_points': tasks[i]['ver_points'], 'description1':cell_string}]
       
        # Single request answer
        if tasks[i]['request'] == "R1":
            cell_type='Code'
            cell_string=f"""#Inserisci le risposte\npercorso = [] # sequenza dei numeri come incontrati dalla cima verso il fondo del triangolo.\nsomma = 0"""
            cell_metadata={"init_cell": True, "trusted": True, "deletable": False}
            add_cell(note,cell_type,cell_string,cell_metadata)
            # Single request verifier
            cell_type='Code'
            cell_string=verif
            cell_metadata={"hide_input": False, "editable": False,  "deletable": False, "trusted": True, "tags": ["noexport"]}
            add_cell(note,cell_type,cell_string,cell_metadata)
            num_of_question += 1
        # for all requests
        #insert_user_bar_cell(note)
    
    yaml_gen['tasks']=tasks_istanza_libera
    return note, yaml_gen

