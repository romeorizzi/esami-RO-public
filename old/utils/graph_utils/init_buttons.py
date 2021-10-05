buttons$i$ = widgets.Button(description="Avvia task")
buttonl$i$ = widgets.Button(description="Carica ultima configurazione")
buttonr$i$ = widgets.Button(description="Reset task")

bllc$i$ = True
#display(button2, output2)

def run_all$i$():
    display(Javascript('''
        function sleep2(milliseconds) {
          var start = new Date().getTime();
          for (var i = 0; i < 1e7; i++) {
            if ((new Date().getTime() - start) > milliseconds){
              break;
            }
          }
        }
        var output_area = this;
		// find my cell element
		var cell_element = output_area.element.parents('.cell');
		// which cell is it?
		var cell_idx = Jupyter.notebook.get_cell_elements().index(cell_element);
        try{
            IPython.notebook.execute_cells([cell_idx+1])
			IPython.notebook.execute_cells([cell_idx+2])
			IPython.notebook.execute_cells([cell_idx+3])
        }catch{}
        '''))
    

def on_run_clicked1$i$(b):
    global bllc$i$
    bllc$i$=True
    run_all$i$()
def on_llc$i$(b):
    global bllc$i$
    bllc$i$=False
    run_all$i$()

def on_reset_clicked$i$(b):
    global bllc$i$
    bllc$i$=True
    run_all$i$()    
    
buttons$i$.on_click(on_run_clicked1$i$)
buttonl$i$.on_click(on_llc$i$)
buttonr$i$.on_click(on_reset_clicked$i$)
widgets.HBox([buttons$i$, buttonl$i$, buttonr$i$])