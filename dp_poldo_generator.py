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
    note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags":['noexport']}

def insert_heading(note, exer_title):
    """It inserts the header and the exercise title
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt = open(PATH_UTILS + 'heading.md', 'r', encoding='utf-8').read()
    content_title = txt.replace('?title?', exer_title)
    note['cells'] += [nb.v4.new_markdown_cell(content_title)]
    note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": []}
    #note['cells'] += [nb.v4.new_markdown_cell('<b>NOTA</b>: qui sotto sono riportate alcune celle di codice con import necessari al funzionamento dei verificatori; ignorali pure. Clicca su "Avvio esercizio" e poi vai pure oltre la barra nera, per svolgere le richieste.')]
    #note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport']}

def insert_n_tasks(note, n_tasks):
    text_n_tasks = """\
    n_tasks = """ + str(n_tasks) + """;
    arr_point= [-1] * n_tasks;"""
    note['cells'] += [nb.v4.new_code_cell(text_n_tasks)]
    note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "tags":['noexport']}

# def insert_separator_bar(note):
#     content = '<h1>_______________________________________________________________________________________ </h1>'
#     note['cells'] += [nb.v4.new_markdown_cell(content)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport']}
#     return

# def insert_user_bar_lib(note):#, path_ex_folder):
#     """It inserts the Python code to add the user bar needed to answer to each task
#     Parameters:
#     note (Jupyter nb.v4): the notebook
#     path_ex_folder (str): the path of the current exercise where the mode has to be added"""
#     user_bar_lib = open(PATH_UTILS + 'user_bar.py', 'r', encoding='utf-8').read()
#     note['cells'] += [nb.v4.new_code_cell(user_bar_lib)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ['noexport']}
#     return

# def insert_user_bar_cell(note):
#     """It inserts the user bar as a code cell
#     Parameters:
#     note (Jupyter nb.v4): the notebook"""
#     user_bar_call = open(PATH_UTILS + 'user_bar_call.md').read()
#     note['cells'] += [nb.v4.new_code_cell(user_bar_call)]
#     note.cells[-1].metadata = {"hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ['noexport']}
#     return

def generate_nb(path_yaml):
    # Notebook creation
    note = nb.v4.new_notebook()
    note['cells'] = []

    # Reading the instance
    exer = read_exercise_yaml(path_yaml)
    s=exer['s']
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

    # Heading and needed import
    insert_heading(note, exer['title']) # heading with title
    insert_import_mode_free(note)
    insert_n_tasks(note, n_tasks)

    # BEGIN instance specific data pre-elaboration
    dictionary_of_types = {
         "SC": "<b>strettamente crescente</b>",
         "ND": "<b>non-decrescente</b>",
         "SD": "<b>strettamente decrescente</b>",
         "NC": "<b>non-crescente</b>",
          "V": "<b>una V-sequenza</b>, se cala fino ad un certo punto, e da lì in poi cresce sempre",
          "A": "<b>ad A</b> (prima sù e poi giù)</it>",
         "SV": "<b>a V stretto</b> <it>(prima strettamente giù e poi strettamente sù)</it>",
         "SA": "<b>ad A stetto</b> <it>(prima strettamente sù e poi strettamente giù)</it>",
          "N": "<b>una N-sequenza</b> (non-decrescente con al più un ripensamento)</it>",
          "Z": "<b>una Z-sequenza</b> <it>(non-crescente con al più un ripensamento)</it>",
         "SN": "<b>una N-sequenza stretta</b> <it>(strettamente crescente con al più un ripensamento)</it>",
         "SZ": "<b>una Z-sequenza stretta</b> <it>(strettamente decrescente con al più un ripensamento)</it>",
     "ZigZag": "<b>a Zig-Zag</b> <it>(primo passo a crescere e poi alterna ad ogni passo)</it>",
     "ZagZig": "<b>a Zag-Zig</b> <it>(primo passo a calare e poi alterna ad ogni passo)</it>",
    "ZigZagEQ": "<b>a Zig-Zag debole</b> <it>(primo passo a crescere e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>",
    "ZagZigEQ": "<b>a Zag-Zig debole</b> <it>(primo passo a calare e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>",
    "132-free": "<b>dal mondo delle permutazioni pattern free per un infinità di problemi in FPT</b>",
    }
    # END instance specific data pre-elaboration

    # Adding the instance to the notebook
    instance=f"s={s}"
    cell_type='Code'
    cell_string=instance
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ["noexport"], "trusted": True}
    add_cell(note, cell_type,cell_string,cell_metadata)

    # Verifier
    cell_type="Code"
    cell_string = """\
    def is_subseq(s, subs):
        found = 0
        pos_r = 0
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
            if answ == "Si":
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
           "V": ("implemented", "<b>a V</b> <it>(prima giù e poi sù)</it>"),
           "A": ("implemented", "<b>ad A</b> (prima sù e poi giù)</it>"),
          "SV": ("implemented", "<b>a V stretto</b> <it>(prima strettamente giù e poi strettamente sù)</it>"),
          "SA": ("implemented", "<b>ad A stetto</b> <it>(prima strettamente sù e poi strettamente giù)</it>"),
           "N": ("implemented", "<b>a N</b> (non-decrescente con al più un ripensamento)</it>"),
           "Z": ("implemented", "<b>a Z</b> <it>(non-crescente con al più un ripensamento)</it>"),
          "SN": ("implemented", "<b>a N stetto</b> <it>(strettamente crescente con al più un ripensamento)</it>"),
          "SZ": ("implemented", "<b>a Z stretto</b> <it>(strettamente decrescente con al più un ripensamento)</it>"),
      "ZigZag": ("implemented", "<b>a Zig-Zag</b> <it>(primo passo a crescere e poi alterna ad ogni passo)</it>"),
      "ZagZig": ("implemented", "<b>a Zag-Zig</b> <it>(primo passo a calare e poi alterna ad ogni passo)</it>"),
    "ZigZagEQ": ("implemented", "<b>a Zig-Zag debole</b> <it>(primo passo a crescere e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>"),
    "ZagZigEQ": ("implemented", "<b>a Zag-Zig debole</b> <it>(primo passo a calare e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>"),
    "132-free": ("not yet done", "<b>dal mondo delle permutazioni pattern free per un infinità di problemi in FPT</b>"),
         "...": ("not thought of yet", "<b>???</b>")
    }

    def Latex_type(seq_type):
        return dictionary_of_types[seq_type][1].replace("_", "\_")


    def is_seq_of_type(s, name_s, seq_type):
        first_down = first_up = first_flat = None
        for i in range(1,len(s)):
            if s[i] < s[i-1]:
                if seq_type=="V" and first_up != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type('V')} poichè ${LaTexVarName(name_s)}[${i-1}$] = {s[i-2]} $<$ {s[i-1]} $= {LaTexVarName(name_s)}[${i}$] > {LaTexVarName(name_s)}[${i+1}$] =$ {s[i]}.")
                if seq_type in {"SC","ND"} or (seq_type in {"ZigZag","ZigZagEQ"} and s[i]%2 == 1) or (seq_type in {"ZagZig","ZagZigEQ"} and s[i]%2 == 0):
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${i}$] $= {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if first_down == None:
                    first_down = i
                elif seq_type=="N":
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_down}$] = {s[first_down-1]} $>$ {s[first_down]} $= {LaTexVarName(name_s)}[${first_down+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if seq_type=="SN" and first_flat != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_flat}$] = {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if s[i] > s[i-1]:
                if seq_type=="A" and first_down != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type('A')} poichè ${LaTexVarName(name_s)}[${i-1}$] =$ {s[i-2]} $>$ {s[i-1]} $= {LaTexVarName(name_s)}[${i}$] < {LaTexVarName(name_s)}[${i+1}$] =$ {s[i]}.")
                if seq_type in {"SD","NC"} or (seq_type in {"ZagZig","ZagZigEQ"} and s[i]%2 == 1) or (seq_type in {"ZigZag","ZigZagEQ"} and s[i]%2 == 0):
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $<$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if first_up == None:
                    first_up = i
                elif seq_type=="Z":
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_up}$] =$ {s[first_up-1]} $<$ {s[first_up]} $= {LaTexVarName(name_s)}[${first_up+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $<$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if seq_type=="SZ" and first_flat != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_flat}$] =$ {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $<$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if s[i] == s[i-1]:
                if seq_type in {"SC","SD","SV","SA","ZigZag","ZagZig"}:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if first_flat == None:
                    first_flat = i
                elif seq_type in {"SN","SZ"}:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_flat}$] =$ {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if seq_type=="SN" and first_down != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_down}$] =$ {s[first_down-1]} $>$ {s[first_down]} $= {LaTexVarName(name_s)}[${first_down+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
                if seq_type=="SZ" and first_up != None:
                    return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_up}$] =$ {s[first_up-1]} $<$ {s[first_up]} $= {LaTexVarName(name_s)}[${first_up+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
        return (1,None)

    def LaTexVarName(var_name):
        return var_name.replace("_", "\_")


    def is_subseq_of_type(s, name_s, subs, name_subs, subs_type, pt_green, pt_red, index_pt, forced_ele_pos = None, start_banned_interval = None, end_banned_interval = None):
        submission_string = f"Hai inserito il certificato ${LaTexVarName(name_subs)}={subs}$."
        submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"

        if len(subs) == 0:
            return submission_string + f"{evaluation_format('No', 0,pt_red, index_pt)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta è vuota."
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
            return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non è sottosequenza di ${LaTexVarName(name_s)}$."
        if forced_ele_pos != None:
            forced_ele_0basedpos = forced_ele_pos-1
            found_magic_point = False
            for guess_0basedpos_in_subs in range(len(subs)):
                if subs[guess_0basedpos_in_subs] == s[forced_ele_0basedpos]:
                    if is_subseq(s[:forced_ele_0basedpos], subs[:guess_0basedpos_in_subs]) and is_subseq(s[forced_ele_0basedpos:], subs[guess_0basedpos_in_subs:]):
                        found_magic_point = True#False
            if not found_magic_point:
                return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non è sottosequenza di ${LaTexVarName(name_s)}$ che ne includa l'elemento in posizione ${forced_ele_pos}$."

        return submission_string + f"{evaluation_format('Si', pt_green,pt_red, index_pt)}"

    def eval_coloring(s, name_s, col, name_col, subs_type, pt_green, pt_red, index_pt):
        submission_string = f"Hai inserito il certificato ${LaTexVarName(name_col)}={col}$."
        submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"

        for c in col:
            subs = [s[i] for i in range(len(s)) if col[i] == c]
            if not is_seq_of_type(subs, "subs", subs_type)[0]:
                return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"Checking the subsequence of the elements colored with {c} within ${LaTexVarName(name_s)}$, that is {subs} ... " + is_seq_of_type(subs, "subs", subs_type)[1]
        return submission_string + f"{evaluation_format('Si', pt_green ,pt_red, index_pt)}"

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
                return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"Attenzione la sottosequenza ${elem}$ non è del tipo richiesto."

        return submission_string + f"{evaluation_format('Si', pt_green,pt_red,index_pt)}"
    """
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "tags": ["noexport"], "trusted": True}
    add_cell(note, cell_type,cell_string,cell_metadata)

    # Description1
    cell_type='Markdown'
    cell_string="Si consideri la seguente sequenza di numeri naturali:<br/><br/>"+str(s)
    cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "trusted": True}
    add_cell(note, cell_type,cell_string,cell_metadata)
    yaml_gen['description1']=cell_string

    # Requests
    for i in range (0,len(tasks)):
        if tasks[i]['request']=="R1":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Trovare una sottosequenza $subs{num_of_question}$ {dictionary_of_types[tasks[i]['type']]} di $s$ che sia la più lunga possibile."
            request_lib = f"Trovare una sottosequenza " + str(dictionary_of_types[tasks[i]['type']]) + " di s che sia la più lunga possibile"
            verif=f"display(Markdown(is_subseq_of_type(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"
        elif tasks[i]['request'] =="R2":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Trovare una sottosequenza $subs{num_of_question}$  {dictionary_of_types[tasks[i]['type']]} di $s$ che sia la più lunga possibile che escluda gli elementi dalla posizione {tasks[i]['start_banned_interval']} alla posizione {tasks[i]['end_banned_interval']}."
            request_lib = f"Trovare una sottosequenza " + str(dictionary_of_types[tasks[i]['type']]) + " di s che sia la più lunga possibile che escluda gli elementi dalla posizione " + str(tasks[i]['start_banned_interval']) + " alla posizione " + str(tasks[i]['end_banned_interval'])
            verif= f"display(Markdown(is_subseq_of_type(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1}, start_banned_interval={tasks[i]['start_banned_interval']}, end_banned_interval={tasks[i]['end_banned_interval']})))"
        elif tasks[i]['request'] == "R3":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Trovare la più lunga sottosequenza {dictionary_of_types[tasks[i]['type']]} che includa l'elemento in posizione {tasks[i]['forced_ele_pos']}"
            request_lib = f"Trovare la più lunga sottosequenza " + str(dictionary_of_types[tasks[i]['type']]) + " che includa l'elemento in posizione " + str(tasks[i]['forced_ele_pos'])
            verif=f"display(Markdown(is_subseq_of_type(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1}, forced_ele_pos={tasks[i]['forced_ele_pos']})))"
        elif tasks[i]['request'] =="R4":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Una sequenza è detta {dictionary_of_types[tasks[i]['type']]}. Trovare la più lunga sequenza di questo tipo che sia una sottosequenza della sequenza data."
            request_lib=f"Una sequenza è detta " + str(dictionary_of_types[tasks[i]['type']]) + ". Trovare la più lunga sequenza di questo tipo che sia una sottosequenza della sequenza data"
            verif=f"display(Markdown(is_subseq_of_type(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"
        elif tasks[i]['request'] =="R5":
            request=f"__Richiesta {num_of_question} [{tasks[i]['tot_points']} punti]__: Qual è il minor numero possibile di colori _C_ per colorare gli elementi della sequenza in input in modo che, per ogni colore, la sottosequenza degli elementi di quel colore sia monotona {dictionary_of_types[tasks[i]['type']]}? Specificare per ogni elemento il colore (come colori, usare i numeri da 1 a _C_)"
            request_lib = f"Qual è il minor numero possibile di colori C per colorare gli elementi della sequenza in input in modo che, per ogni colore, la sottosequenza degli elementi di quel colore sia monotona " + str(dictionary_of_types[tasks[i]['type']]) + "? Specificare per ogni elemento il colore (come colori, usare i numeri da 1 a C)"
            verif=f"display(Markdown(eval_coloring(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=2, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"

        # aggiungere altre possibili richieste e relativi verificatori
        else:
            assert False

        # Single request text
        cell_type='Markdown'
        cell_string= request
        cell_metadata ={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "trusted": True}
        add_cell(note, cell_type,cell_string,cell_metadata)
        tasks_istanza_libera+=[{'tot_points' : tasks[i]['tot_points'],'ver_points': tasks[i]['ver_points'], 'description1':request_lib.replace("<b>","").replace("</b>","")}]

        # Single request answer
        cell_type='Code'
        cell_string=f'#Inserisci la risposta\nsubs{num_of_question}=[]'
        cell_metadata={"init_cell": True, "trusted": True, "deletable": False}
        add_cell(note,cell_type,cell_string,cell_metadata)

        # Single request verifier
        cell_type='Code'
        cell_string=verif
        cell_metadata={"init_cell": True, "hide_input": True, "editable": False,  "deletable": False, "trusted": True}
        add_cell(note,cell_type,cell_string,cell_metadata)
        num_of_question += 1

    yaml_gen['tasks']=tasks_istanza_libera
    return note, yaml_gen
