#parsing del grafo xml o graphml, viene creato graph_data, original_nodes e original_edges
if bllc$i$:
    pass
else:
    try:
        list_of_files$i$ = glob.glob('allegati/ck_points/graph_data_'+str($i$)+'_*')
        latest_file$i$ = max(list_of_files$i$, key=os.path.getctime)
    except:
        pass
    try:
        with open(latest_file$i$) as json_file:     
            graph_data$i$ = json.load(json_file)
    except:
        print("Nessun file di configurazione trovato!")