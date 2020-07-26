import os
import time
from urllib.request import urlopen
import nbformat
from traitlets.config import Config
from nbconvert import HTMLExporter
from nbconvert import RSTExporter, NotebookExporter
from IPython.display import Image, HTML, Javascript
from datetime import datetime

import shutil
last ='preview_last/' #path of last submission
old = 'preview_old/' #path of prevous submissions

#hide alert buttons
def hide_w(w):
    for e in w:
        e.layout.visibility = 'hidden'
        
#show alert buttons
def show_w(w):
    for e in w:
        e.layout.visibility = 'visible'

def are_you_sure():
    show_w(alert_buttons)

label = widgets.Label(value="Un tuo elaborato era già stato precedentemente prodotto. Vuoi rimpiazzarlo con il presente?")
yes = widgets.Button(description="Si", tooltip="Produce il nuovo elaborato. Esso diviene la versione attuale prendendo il posto del precedente")
no = widgets.Button(description="No")

alert_buttons = [label,yes,no]
hide_w(alert_buttons)

#move all files from last to old and save the new preview
def yes_clicked(b):
    files = os.listdir(last)
    for f in files:
        if f == '.ipynb_checkpoints':
            continue
        if not os.path.isdir('./preview_old'):
            os.mkdir(old)
        shutil.move(last+f, old)
    display(Javascript('IPython.notebook.save_checkpoint();'))
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    hname = '?FILENAME?'[:-6] + '_' + date_time
    ! jupyter nbconvert ?FILENAME? --to html_embed --output=$hname --output-dir=./preview_last/ --no-input
    display(Javascript('window.open("./preview_last/' + hname + '.html")'))
    hide_w(alert_buttons)
def no_clicked(b):
    hide_w(alert_buttons)


def generate_preview_HTML(_):
    if not os.path.isdir('./preview_last'):
        os.mkdir(last)
    directory= os.listdir(last)
    if len(directory) <1:
        display(Javascript('IPython.notebook.save_checkpoint();'))
        now = datetime.now() # current date and time
        date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        hname = '?FILENAME?'[:-6] + '_' + date_time
        ! jupyter nbconvert ?FILENAME? --to html_embed --output=$hname --output-dir=./preview_last/ --no-input
        display(Javascript('window.open("./preview_last/' + hname + '.html")'))
    else:
        are_you_sure()
    

button = widgets.Button(description="Salva & Esporta", tooltip="Esporta il foglio Jupyter in HTML nella cartella preview")
output = widgets.Output()
button.on_click(generate_preview_HTML)
yes.on_click(yes_clicked)
no.on_click(no_clicked)
h_box1 = widgets.HBox([button])
h_box2 = widgets.HBox([label,yes,no])
display(widgets.VBox([h_box1,h_box2]))
