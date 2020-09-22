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
                                       's_cell': 'cell$i$'})

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
            <div id="sigma-container$i$" style="height:750px; width:100%"></div>
        </div>
    </div>

<script> $js_text$i$ </script>
''')
#render HTML con sostituzione variabili
HTML(html_template$i$.substitute({'js_text$i$': js_text$i$}))