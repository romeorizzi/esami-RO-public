#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors:
Map: Rosario Di Matteo, Marco Emporio, Adriano Tumminelli;
Integration: Alice Raffaele, Romeo Rizzi.

"""

import html

def generate(exam_date, list_of_exercises_infos):
    """Returns the generated html"""

    outHTML = ""

    #html header
    with open("utils/map_templates/header.html", 'r') as f:
        outHTML += f.read()

    #html exercise template
    exercise_template = ""
    with open("utils/map_templates/exercise.html", 'r') as f:
        exercise_template = f.read()

    #html task template
    task_template = ""
    with open("utils/map_templates/task.html", 'r') as f:
        task_template = f.read()

    for exercise in list_of_exercises_infos:
        print(f'\n exercise={exercise["title"]}')
        ex_tags = ""
        for tag in exercise["tags"]:
            ex_tags += '<div class="competence">' + tag + '</div> '

        tasks_html = ""
        total_points_calculated = 0
        for task_idx in range(len(exercise["tasks"])):
            task = exercise["tasks"][task_idx][task_idx+1]
            task_values = ""
            for i in range(0, task["tot_points"] + 1):
                task_values += '<option value="'+str(i)+'">'+str(i)+'</option>\n'
            total_points_calculated += task["tot_points"]
            tasks_html += task_template.format(
                ex_task_name = "Task " + html.escape(str(task_idx)),
                ex_task_values = task_values,
                ex_task_max_points = str(task["tot_points"] ),
                ex_task_description = html.escape(task["description1"])
            ) + "\n"

        #aggiunta delle varie modalità per ogni esercizio
        modes_html = ""
        i=0
        for mode in exercise["mode"]:
            if i == 0:
                modes_html += '<option value="'+str(i)+' selected">'+mode+'</option>\n'
            else:
                modes_html += '<option value="'+str(i)+'">'+mode+'</option>\n'
            i+=1
        
        #aggiunta di un campo nascosto per salvare i link delle pagine relative alle modalità
        links_html = ""
        i=0
        #prova=""
        for link in exercise["link"]:
            links_html += '<input type="hidden" name='+str(i)+' value='+link+' />\n'
            i+=1
            #prova=link
        
        outHTML += exercise_template.format(
            ex_title = html.escape(exercise["title"]),
            ex_tags = ex_tags,
            ex_tot_points = total_points_calculated,
            ex_link = exercise["link"][0],
            ex_links = links_html, 
            ex_tasks = tasks_html,
            ex_mode = modes_html
        )

    #html footer
    with open("utils/map_templates/footer.html", 'r') as f:
        outHTML += f.read().replace("?EXAM_DATE?", exam_date)

    return outHTML
