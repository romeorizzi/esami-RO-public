import os
import time
from urllib.request import urlopen
import nbformat
from traitlets.config import Config
from nbconvert import HTMLExporter
from nbconvert import RSTExporter, NotebookExporter
from IPython.display import Image, HTML, Javascript
from datetime import datetime

def generate_preview_HTML(_):
    display(Javascript('IPython.notebook.save_checkpoint();'))
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    hname = '?FILENAME?'[:-6] + '_' + date_time
    ! jupyter nbconvert ?FILENAME? --to html_embed --output=$hname --output-dir=./preview/ --no-input
    display(Javascript('window.open("./preview/' + hname + '.html")'))

button = widgets.Button(description="Salva & Esporta", tooltip="Esporta il foglio Jupyter in HTML nella cartella preview")
output = widgets.Output()
button.on_click(generate_preview_HTML)
display(widgets.HBox([button]))
