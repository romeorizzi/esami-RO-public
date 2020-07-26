import os
from IPython.core.display import display, HTML, Markdown, clear_output, Javascript
import ipywidgets as widgets
from IPython.display import IFrame, display

def on_change(change): # si attiva quando cambio scelta dell'elemento da selezionare
    global attach
    if change['type'] == 'change' and change['name'] == 'value':
        #print ("Stai scegliendo %s" % change['new'])
        attach = change['new']
        return attach

def on_button_update(_):
    clear_output()
    #display(Javascript('''var c = IPython.notebook.get_selected_index();
                       #IPython.notebook.execute_cells([c])'''))
    add_attachment()

def open_attachment(attach_name):
    path_attachments = "allegati"
    path_file=str(path_attachments + "/" + attach_name)
    ext = os.path.splitext(path_file)[-1].lower()
    #print(path_file)
    #print(ext)
    #print(ext.replace('.', ''))
    if(ext=='.pdf'):
        pdf=IFrame(path_file, width=700, height=400)
        display(pdf)
    else:
        #file = open(path_file, "rb")
        display(Markdown("![alt text](" + path_file + ")"))
        delete = widgets.Button(description='Rimuovi allegato')
        delete.on_click(on_button_delete)
        display(delete)

        #image = file.read()
        #w=widgets.Image(
        #    value=image,
        #    format=ext.replace('.', ''),
        #    width=300,
        #    height=400,
        #)
        #display(w)

def on_button_confirm(_):
    global attach
    clear_output()
    print('Allegato: ' + str(attach))
    open_attachment(attach)

def add_attachment():
    path_attachments = "allegati"
    global attach # allegato attuale scelto
    update = widgets.Button(description='Aggiorna') #bottone visualizzato in ogni caso
    delete = widgets.Button(description='Rimuovi allegato')
    attach_list = os.listdir(path_attachments)

    if(attach_list): #si attiva se c'è almeno un elemento in lista quindi nella cartella allegati
        confirm = widgets.Button(description='Conferma')
        chosen_attach_wid = widgets.Dropdown(
            options = attach_list,
            value = attach_list[0],
            description = 'Allegati:',
            disabled = False,
        )
        attach = attach_list[0]
        chosen_attach_wid.observe(on_change)
        update.on_click(on_button_update)
        confirm.on_click(on_button_confirm)
        delete.on_click(on_button_delete)
        all_buttons = [update, chosen_attach_wid, confirm, delete]
        display(widgets.HBox(all_buttons))
    else:
        print(f"ATTENZIONE: non sono presenti file nella cartella allegati. Ti ricordiamo che la cartella utile per gli allegati da te prodotti per questo esercizio in modo_libero di svolgimento è la cartella @path_ex_folder@/modo_libero/allegati/")
        update.on_click(on_button_update)
        delete.on_click(on_button_delete)
        all_buttons = [update, delete]
        display(widgets.HBox(all_buttons))

def on_button_delete(_):
    #delete_above_cell()
    delete_this_cell()

def delete_above_cell():
    display(Javascript('''var c = IPython.notebook.get_selected_index();
                                IPython.notebook.get_cell(c-1).metadata.editable = true;
                                IPython.notebook.get_cell(c-1).metadata.deletable = true;
                                IPython.notebook.delete_cell([c-1]);'''))
def delete_this_cell():
    display(Javascript('''var c = IPython.notebook.get_selected_index();
                                IPython.notebook.get_cell(c).metadata.editable = true;
                                IPython.notebook.get_cell(c).metadata.deletable = true;
                                IPython.notebook.delete_cell([c]);'''))

def on_button_raw_attach(_):
    add_attach_cell_din('add_attachment()')

def on_button_md(_):
    add_md_cell_din()

def on_button_code(_):
    add_code_cell_din()

def on_button_raw(_):
    add_raw_cell_din()

def add_raw_cell_din():
    display_id = int(time.time()*1e9) # Hack
    display(Javascript('''var idx = IPython.notebook.get_selected_index();
                       var c = IPython.notebook.insert_cell_at_index("raw", idx);
    c.set_text('');
    var t_index = IPython.notebook.get_cells().indexOf(c);
    IPython.notebook.to_raw(t_index);
    IPython.notebook.get_cell(t_index).render();
    IPython.notebook.get_cell(t_index).metadata.deletable = true;
    IPython.notebook.get_cell(t_index).set_text('');;'''),display_id=display_id) # Hack
    # Necessary hack to avoid self-generation of cells at notebook re-opening
    # See http://tiny.cc/fnf3nz
    display(Javascript(""" """), display_id=display_id, update=True)
    return

def add_attach_cell_din(code = ''):
    display_id = int(time.time()*1e9) # Hack
    display(Javascript('''var c = IPython.notebook.insert_cell_above();
    c.set_text(' ''' + code + ''' ');
    var t_index = IPython.notebook.get_cells().indexOf(c);
    IPython.notebook.to_code(t_index);
    IPython.notebook.get_cell(t_index).render();
    IPython.notebook.execute_cells([t_index]);
    IPython.notebook.get_cell(t_index).metadata.editable = false;'''),display_id=display_id) # Hack
    # Necessary hack to avoid self-generation of cells at notebook re-opening
    # See http://tiny.cc/fnf3nz
    display(Javascript(""" """), display_id=display_id, update=True)
    return

def add_code_cell_din(code = ''):
    display_id = int(time.time()*1e9)
    display(Javascript('''var c = IPython.notebook.insert_cell_above();
    c.set_text(' ''' + code + ''' ');
    var t_index = IPython.notebook.get_cells().indexOf(c);
    IPython.notebook.to_code(t_index);
    IPython.notebook.get_cell(t_index).render();
    IPython.notebook.execute_cells([t_index]);
    IPython.notebook.get_cell(t_index).metadata.deletable = true;
    IPython.notebook.get_cell(t_index).set_text('');'''),display_id=display_id)
    # Necessary hack to avoid self-generation of cells at notebook re-opening
    # See http://tiny.cc/fnf3nz
    display(Javascript(""" """), display_id=display_id, update=True)
    return

def add_md_cell_din():
    display_id = int(time.time()*1e9)
    display(Javascript('''var c = IPython.notebook.insert_cell_above();
    c.set_text(' ');
    var t_index = IPython.notebook.get_cells().indexOf(c);
    IPython.notebook.to_markdown(t_index);
    IPython.notebook.get_cell(t_index).render();
    IPython.notebook.get_cell(t_index).metadata.deletable = true;
    IPython.notebook.get_cell(t_index).set_text('');'''),display_id=display_id) # Hack
    # Necessary hack to avoid self-generation of cells at notebook re-opening
    # See http://tiny.cc/fnf3nz
    display(Javascript(""" """), display_id=display_id, update=True)
    return

def add_cell(code='', position='below', celltype='markdown', is_execute = False):
    """Create a cell in the IPython Notebook.
    code: unicode, Code to fill the new cell with.
    celltype: unicode, Type of cells "code" or "markdown".
    position: unicode, Where to put the cell "below" or "at_bottom"
    is_execute: boolean, To decide if the cell is executed after creation
    """

    # Create a unique id based on epoch time
    display_id = int(time.time()*1e9)

    if is_execute:
        display(Javascript("""
        var basis = IPython.notebook.insert_cell_{0}("{1}");
        basis.set_text(atob("{2}"));
        basis.execute();
        """.format(position, celltype, " ")),display_id=display_id)

    else:
        display(Javascript("""
        var basis = IPython.notebook.insert_cell_{0}("{1}");
        basis.set_text(atob("{2}"));
        """.format(position, celltype, " ")),display_id=display_id)


    # Necessary hack to avoid self-generation of cells at notebook re-opening
    # See http://tiny.cc/fnf3nz
    display(Javascript(""" """), display_id=display_id, update=True)

def code_button_delete():
    button_delete = widgets.Button(description="Rimuovi l'allegato", tooltip="Seleziona la cella e clicca su Elimina")
    button_delete.on_click(on_button_delete)
    #print("Vuoi eliminare la cella selezionata?")
    display(button_delete)

def loader_main():
    button_raw_attach = widgets.Button(description="Rispondi (Allegato)", tooltip="Collega un file dalla cartella attachments")
    button_md = widgets.Button(description="Rispondi (Markdown)", abstooltip="Aggiungi una cella per scrivere del testo in Markdown")
    button_code = widgets.Button(description="Rispondi (Code)", tooltip="Aggiungi una cella per scrivere del codice in Python")
    button_raw = widgets.Button(description="Rispondi (Raw)", tooltip="Aggiungi una cella per scrivere del testo libero (SCONSIGLIATA: righe troppo lunghe potrebbero fuoriuscire nella rendition, usala solo se non riesci a controllare il Markdown)")
    button_raw_attach.on_click(on_button_raw_attach)
    button_md.on_click(on_button_md)
    button_code.on_click(on_button_code)
    button_raw.on_click(on_button_raw)

    all_buttons = [button_code, button_md, button_raw, button_raw_attach]
    display(widgets.HBox(all_buttons))
