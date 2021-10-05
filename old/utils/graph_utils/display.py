js_text_template$i$ = Template(open('../../graph_utils/js/sigma-graph.js','r').read())
#faccio il dump della struttura che ho creato dentro il js
js_text$i$ = js_text_template$i$.substitute({'graph_data': json.dumps(graph_data$i$),
                                            'exercise' : $i$,
                                            'container':'sigma-container$i$',
                                            'data':0,
                                            'x':center$i$[0]+center$i$[0]*0.6,
                                            'y':center$i$[1],
                                            's':'s$i$',
                                            'n':'n$i$',
                                            'ef':'`'+str(friends_e$i$)+'`',
                                            'nf':'`'+str(friends_n$i$)+'`',
                                            's_cell': 'cell$i$',
                                            'states': str(states$i$),
                                            'scope': str(scope$i$)})

html_template$i$ = Template('''
<style>
    .container { width:100% !important; }
</style>
<link rel="stylesheet" href="../../graph_utils/css/style.css">
    <div class="row row-no-gutters" style="border-color: #1e6add; border-width: 2px;">
        <div class="col-sm-1" style="border-color: #1e6add; border-width: 2px;">
            ''' + html_text$i$ + '''
        </div>
        <div class="col-sm-11" style="position:border-color: #1e6add; border-width: 2px;">
            <!-- The Modal -->
            <div id="myModal$i$" class="modal">

            <!-- Modal content -->
            <div class="modal-content">
                <div class="modal-header">
                    <a id="close$i$" class="close" style="position: absolute;top: 20px;right: 20px;font-size: 50px;color: black;font-weight: bold;">&times;</a>
                    <strong style="font-size: 20px;">Inserisci il valore del flusso</strong>
                </div>
                <div class="modal-body">
                    <input type="radio" id="lr$i$" name="dir" value="0" style="margin-bottom: 20px; margin-top: 20px;margin-right: 10px;"></input>
                    <label id="lrLbl$i$">S->G</label>
                    <br>
                    <input type="radio" id="rl$i$" name="dir" value="1" style="margin-bottom: 20px;margin-right: 10px;"></input>
                    <label id="rlLbl$i$">G->S</label>
                    <br>
                    <input type="text" id="value$i$" name="flowVal" style="border: none;border-bottom: 1px solid black;background: transparent;outline: none;height: 30px;color: black;font-size: 15px;width: 100%;">
                </div>

                <div class="modal-footer" style="display:flex; justify-content:flex-end; width:100%; padding:0;">
                    <input type="button" id="cnf$i$" value="Conferma" class="button"/>
                </div>
            </div>

            </div>
            <div id="sigma-container$i$" style="height:750px; width:100%"></div>
        </div>
    </div>

<script> $js_text$i$ </script>
''')
#render HTML con sostituzione variabili
HTML(html_template$i$.substitute({'js_text$i$': js_text$i$}))