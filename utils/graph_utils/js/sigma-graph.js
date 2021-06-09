/*
Position of element in flags_for_js at moment not used
Used try and catch
0: select_color_node
1: drag_node: possibility to drag the node
2: remove_edge: delete a selected edge
3: remove_node: delete a selected node
4: add_node: add a node
5: add_edge: add an edge
6: choice: possibility to chioice between yes or no
7: edit_label: label on edge or node are editable (TODO)
*/
/*
For camera e drag node use no_editable
0: camera
1: drag node
*/
var g = $graph_data;
var not_editable = $data;
var default_color_node = "#000000";
var default_color_edge = "#828282";
var color_first_set = "#FF5722";
var color_second_set = "#FFD600";
var size_edge = 1;
var size_node = 2;
var directed = false;
var $n = $exercise;
var states$n = $states;
var scope$n = $scope;
//states for buttons
var all_download_state  = ['download_svg','download_png','download_adj'];
var selection_state     = ['select', 'unselect'];
var multiple_drag_state = ['drag'];
var editweight_state    = ['editweight'];

var multiple_sel = false;
centerX = document.getElementById('$container').offsetLeft + document.getElementById('$container').offsetWidth / 2;
centerY = document.getElementById('$container').offsetTop + document.getElementById('$container').offsetHeight / 2;
function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

$s = new sigma({
    graph: g,
    renderer: {
        container: document.getElementById('$container'),
        type: 'canvas'
    },
    settings: {
        minNodeSize: 2,
        maxNodeSize: 6,
        minEdgeSize: 6,
        maxEdgeSize: 6,
        minArrowSize: 1,
        zoomMin: 0.01,
        zoomMax: 5,
        zoomingRatio: 0.9,
        enableEdgeHovering: true,
        doubleClickEnabled: false,
        defaultNodeColor: default_color_node,
        edgeHoverColor: 'edge',
        defaultNodeHoverColor: "#4CAF50",
        defaultEdgeHoverColor: "#1e6add",
        borderSize: 0,
        doubleClickEnabled: false,
        arrowSizeRatio: 5,
        sideMargin: 15,
        autoRescale: false,
        rescaleIgnoreSize: false,
        enableHovering: true,
        autoResize: false,
        defaultEdgeLabelSize: 12,
        defaultLabelSize: 12,
        labelThreshold: 1,
        edgeHoverSizeRatio: 1,
        edgeHoverExtremities: false,
        edgeLabelSize: 'fixed',
        labelSizeRatio: 3,
        defaultLabelSize: 17,
    },
});


$s.cameras[0].goTo({ x: 1200,y: -100, angle:0, ratio: 0.9 });
// Fully disable autoRescale
//pezzi di arco
var ef = $ef;
var nf = $nf;

var dict_ef = JSON.parse(ef.replace(/'/g, "\""));
var dict_nf = JSON.parse(nf.replace(/'/g, "\""));
function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
if (not_editable[0] == "true") {

    $s.settings('enableHovering', false)
}

if (not_editable[1] != "true") {
    sigma.plugins.dragNodes($s, $s.renderers[0]);
}

var kernel = IPython.notebook.kernel;
var nodes_added = 1
var edges_added = 1
var remove_node = false
var remove_edge = false
var source = false
var target = false
var set_one = false // red
var set_two = false // yellow
var unselect_set = false // black
var changeW$n = false;
$s.states = {};
//////////////////////////////////////BUILD ADJANCY MATRIX\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\S
//this method build the adjacency matirx and the mapping
// between the source and the target for each edges
var return_adj$n = $s.buildAdj(
    {
    nodes : $s.graph.nodes(),
    edges : $s.graph.edges(),
    }
);
var adj$n               = return_adj$n[0];
var map$n               = return_adj$n[1];
var hidden_type$n       = return_adj$n[2];
var max_label_length$n  = return_adj$n[3];
var changedWeight_adj$n = return_adj$n[4];
var selected_edge$n     = return_adj$n[5];


//current state with original weight
$s.states["adj"] = adj$n;
//initialization of the weight with the adj matrix
$s.states["changedW_adj"] = changedWeight_adj$n;
$s.states["selectedEdges"] = selected_edge$n;
$s.refresh();



var return_changedWeight$n = [];
var changed_matrix$n = [];
// change edge's labels
//returns the matrix with the modified value if a change has been made, 
// or an empty array if none occurs
$s.bind('clickEdge', function(event){
    return_changedWeight$n = $s.changeWeightEdge({
        changeW     : changeW$n,
        adj         : adj$n,
        map         : map$n,
        n_var       : $n,
        edge        : event.data.edge,
        s_var       : $s,
        matrixInit  : changedWeight_adj$n
    });
    changed_matrix$n = return_changedWeight$n[0]
    $s.states["changedW_adj"] = changed_matrix$n;
    // var e_source = event.data.edge.source;
    // var e_target = event.data.edge.target; 
    // //the follow if structure checks if an already selected arrowed edge have to change
    // // if(selected_edge$n[map$n[e_source]][map$n[e_target]] > 0 || selected_edge$n[map$n[e_target]][map$n[e_source]] > 0){
    // //     if(selected_edge$n[map$n[e_source]][map$n[e_target]] > selected_edge$n[map$n[e_target]][map$n[e_source]]){
    // //         selected_edge$n[map$n[e_source]][map$n[e_target]] = 0;
    // //         selected_edge$n[map$n[e_target]][map$n[e_source]] = 1;
    // //     }
    // //     else if(selected_edge$n[map$n[e_source]][map$n[e_target]] < selected_edge$n[map$n[e_target]][map$n[e_source]]){
    // //         selected_edge$n[map$n[e_source]][map$n[e_target]] = 1;
    // //         selected_edge$n[map$n[e_target]][map$n[e_source]] = 0;
    // //     }   
    // //     else if(selected_edge$n[map$n[e_source]][map$n[e_target]] == selected_edge$n[map$n[e_target]][map$n[e_source]]){ 
    // //         if(changedWeight_adj$n[map$n[e_source]][map$n[e_target]] > changedWeight_adj$n[map$n[e_target]][map$n[e_source]]){
    // //             selected_edge$n[map$n[e_source]][map$n[e_target]] = 1;
    // //             selected_edge$n[map$n[e_target]][map$n[e_source]] = 0;
    // //         }
    // //         else if(changedWeight_adj$n[map$n[e_source]][map$n[e_target]] < changedWeight_adj$n[map$n[e_target]][map$n[e_source]]){
    // //             selected_edge$n[map$n[e_source]][map$n[e_target]] = 0;
    // //             selected_edge$n[map$n[e_target]][map$n[e_source]] = 1;
    // //         }
    // //     }
    // // }
    // $s.states["selectedEdges"] = selected_edge$n;
    $s.refresh();
});



//set color node
//this functions let the users to select the nodes on the graph
//furthermore they contain the functionality to update the "selection_nodes states"
var return_vecrSelect$n = $s.buildVectSelect({
    nodes : $s.graph.nodes(),
    map   : map$n
})
var selected_node$n = return_vecrSelect$n[0];
$s.states["selectedNodes"] = selected_node$n;
$s.refresh();


$s.bind('clickNode', function(e) {
        var node = e.data.node;
        var nodeId = node.id;
        if (target && directed) {
            var new_edge_id = "e_a_" + source_id + "" + nodeId;
            $s.graph.addEdge({
                id: new_edge_id,
                source: source_id,
                target: nodeId,
                type: "arrow",
                label: "1",
                weight: "1",
                color: default_color_edge,
                size: size_edge,
                hover_color: "#4CAF50"
            });
            $s.refresh();
            source_id = null;
            target_id = null;
            target = false;
            directed = false;
        }
        if (target) {
            var new_edge_id = "e_a_" + source_id + "" + nodeId;
            $s.graph.addEdge({
                id: new_edge_id,
                source: source_id,
                target: nodeId,
                type: "line",
                label: "1",
                weight: "1",
                color: default_color_edge,
                size: size_edge,
                hover_color: "#4CAF50"
            });
            $s.refresh();
            source_id = null;
            target_id = null;
            target = false;
        } else if (source) {
            source_id = nodeId;
            source = false;
            target = true;
        } else if (remove_node) {
            for (n in dict_nf) {
                if (n == nodeId) {
                    for (f of new Set(dict_nf[n])) {
                        var true_node = $s.graph.nodes(f);
                        try {
                            if (true_node.piece) {
                                $s.graph.dropNode(f);
                            }
                        } catch {
                            continue;
                        }
                    }
                }
            }
            $s.graph.dropNode(nodeId);
            $s.refresh();
            remove_node = false;
            return;
        // SELECT NODE
        } else if (set_one) {
            node.color = current_color;
            //set to one the position of the node that was selected
            if(selected_node$n[map$n[nodeId]][1] < 1){
                selected_node$n[map$n[nodeId]][1] = 1;
            }
            $s.states['selectedNodes'] = selected_node$n;
            $s.refresh();
        // } else if (set_two) {
        //     node.color = current_color;
        //     $s.refresh()
        // UNSELECT NODE
        } else if (unselect_set) {
            node.color = default_color_node;// current_color;
            if(selected_node$n[map$n[nodeId]][1] > 0){
                selected_node$n[map$n[nodeId]][1] = 0;
            }
            $s.states['selectedNodes'] = selected_node$n;
            $s.refresh();
        }
    });

var to_drop = [];

$s.bind('clickEdge', function(event) {
    var edge = event.data.edge;
    var edgeId = edge.id
    if (edge.piece && remove_edge) {
        for (key in dict_ef) {
            if (key == edgeId) {
                for (f of dict_ef[key]) {
                    var e = $s.graph.edges(f)
                    var source = $s.graph.nodes(e.source)
                    var target = $s.graph.nodes(e.target)
                    if (source.piece) {
                        to_drop.push(source.id)
                    }
                    if (target.piece) {
                        to_drop.push(target.id)
                    }
                    $s.graph.dropEdge(f)
                }
            }
        }
        to_drop_set = new Set(to_drop)
        for (node of to_drop_set) {
            $s.graph.dropNode(node)
        }
        to_drop_set = new Set()
        to_drop = []
        remove_edge = false
        $s.refresh()

    }
    if (remove_edge) {
        $s.graph.dropEdge(edgeId)
        $s.refresh()
        to_remove_e = false
        return
    } 
    else if (set_one) {
        for (key in dict_ef) {
            if (key == edgeId) {
                for (f of dict_ef[key]) {
                    var e = $s.graph.edges(f)
                    e.color = current_color
                    var source = $s.graph.nodes(e.source)
                    var target = $s.graph.nodes(e.target)
                    if (source.piece) {
                        source.color = current_color;
                    }
                    if (target.piece) {
                        target.color = current_color;
                    }
                }
            }
        }
        edge.color = current_color;
        
        if(edge.source in map$n && edge.target in map$n){
            selected_edge$n[map$n[edge.target]][map$n[edge.source]] = 1;
            selected_edge$n[map$n[edge.source]][map$n[edge.target]] = 1;
        }else{
            //hidden nodes
            var list = dict_nf[edge.source];
            var source = list[0];
            var target = list[list.length-1];
            selected_edge$n[map$n[source]][map$n[target]] = 1;
            selected_edge$n[map$n[target]][map$n[source]] = 1;
        }
        
        $s.states["selectedEdges"] = selected_edge$n;
        $s.refresh()
    } 
    // else if (set_two) {
    //     for (key in dict_ef) {
    //         if (key == edgeId) {
    //             for (f of dict_ef[key]) {
    //                 var e = $s.graph.edges(f)
    //                 e.color = current_color
    //                 var source = $s.graph.nodes(e.source)
    //                 var target = $s.graph.nodes(e.target)
    //                 if (source.piece) {
    //                     source.color = current_color
    //                 }
    //                 if (target.piece) {
    //                     target.color = current_color
    //                 }
    //             }
    //         }
    //     }
    //     edge.color = current_color;
    //     $s.refresh()
    // } 
    else if (unselect_set) {
        for (key in dict_ef) {
            if (key == edgeId) {
                for (f of dict_ef[key]) {
                    var e = $s.graph.edges(f)
                    e.color = default_color_edge
                    var source = $s.graph.nodes(e.source)
                    var target = $s.graph.nodes(e.target)
                    if (source.piece) {
                        source.color = default_color_edge;
                    }
                    if (target.piece) {
                        target.color = default_color_edge;
                    }
                }
            }
        }
        edge.color = default_color_edge;
       
        if(edge.source in map$n && edge.target in map$n){
            selected_edge$n[map$n[edge.target]][map$n[edge.source]] = 0;
            selected_edge$n[map$n[edge.source]][map$n[edge.target]] = 0;
        }else{
            //hidden nodes
            var list = dict_nf[edge.source];
            var source = list[0];
            var target = list[list.length-1];
            selected_edge$n[map$n[source]][map$n[target]] = 0;
            selected_edge$n[map$n[target]][map$n[source]] = 0;
        }
    
        $s.states["selectedEdges"] = selected_edge$n;
        $s.refresh()
    } 
    /*else if (set_weight) {
        change_label(edge)
        $s.refresh()
    }*/
});

//add edge
try {
    document.getElementById("btn_add_e" + $n).addEventListener("click", function() {
        set_one = false
        set_two = false
        unselect_set = false
        source = true
        target = false
        changeW$n = false
    });
} catch (e) {};
//add edge
try {
    document.getElementById("btn_add_e_dir" + $n).addEventListener("click", function() {
        set_one = false
        set_two = false
        unselect_set = false
        source = true
        target = false
        directed = true
        changeW$n = false

    });
} catch (e) {};
//yes choice - no choice
try {
    document.getElementById("yes" + $n).addEventListener("click", function() {
        set_one = false
        set_two = false
        unselect_set = false
        changeW$n = false
        command = "choice=True"
        kernel.execute(command)
    });

    //no choice
    document.getElementById("no" + $n).addEventListener("click", function() {
        set_one = false
        set_two = false
        unselect_set = false
        changeW$n = false
        command = "choice=False"
        kernel.execute(command)
    });
} catch (e) {};
//add node
try {
    document.getElementById("btn_add" + $n).addEventListener("click", function() {
        set_one = false
        set_two = false
        unselect_set = false
        changeW$n = false
        var newNodeId = prompt("Enter node id:", "");
        if (newNodeId != null) {
            try {
                $s.graph.addNode({
                    id: newNodeId,
                    label: newNodeId,
                    x: 1,
                    y: 1,
                    size: size_node
                });
            } catch (u) {
                alert("Node already exists")
                return
            }
        } else {
            alert("Bad value!");
            return
        }
        nodes_added = nodes_added + 1;
        $s.refresh();
    });
} catch (e) {};
//remove node
try {
    document.getElementById("btn_remove" + $n).addEventListener("click", function() {
        set_one = false
        set_two = false
        unselect_set = false
        remove_node = true;
        changeW$n = false
        remove_edge = false;
    });
} catch (e) {};

//remove edge
try {
    document.getElementById("btn_remove_e" + $n).addEventListener("click", function() {
        set_one = false
        set_two = false
        unselect_set = false
        remove_edge = true;
        remove_node = false;
        changeW$n = false;
    });
} catch (e) {};


///activation of utility buttons and association of functions to them (the follow 4 if)
//the buttons related to the selection_state
if(states$n.includes('selection')){
    if(selection_state.includes('select')){
        try {
            document.getElementById("btn_set_one" + $n).style.backgroundColor = color_first_set
            document.getElementById("btn_set_one" + $n).addEventListener("click", function() {
                set_one = true;
                set_two = false;
                changeW$n = false;
                unselect_set = false
                remove_edge = false;
                remove_node = false;
                current_color = color_first_set
            });
            // var for_bg = document.getElementById("btn_set_two" + $n);
            // for_bg.style.backgroundColor = color_second_set;
            // for_bg.style.color = "black";
            // document.getElementById("btn_set_two" + $n).addEventListener("click", function() {
            //     set_one = false
            //     set_two = true
            //     unselect_set = false
            //     changeW$n = false
            //     remove_edge = false;
            //     remove_node = false;
            //     current_color = color_second_set
            // });
        } catch (e) {};
    }
    else{
        try{
            var btn = document.getElementById("btn_set_one" + $n);
            btn.parentNode.removeChild(btn);

            // btn = document.getElementById("btn_set_two" + $n);
            // btn.parentNode.removeChild(btn);
        }catch(e){};
    }
    if(selection_state.includes('unselect')){
        try{
            var for_bg = document.getElementById("btn_unselect_set" + $n);
            for_bg.style.backgroundColor = default_color_node;
            document.getElementById("btn_unselect_set" + $n).addEventListener("click", function() {
                set_one = false
                set_two = false
                unselect_set = true
                source = false//true
                target = false
                directed = false //true
                current_color_node = default_color_node;
                current_color_edge = default_color_edge;
            });
        } catch(e){};
    }
    else{
        try{
            btn = document.getElementById("btn_unselect_set" + $n);
            btn.parentNode.removeChild(btn);
        }catch(e){};
    }
}
//the buttons related to the all_download_state
if(states$n.includes('all_download')){
    if(all_download_state.includes('download_svg')){
        try {
            document.getElementById("download_svg" + $n).addEventListener("click",
                function(){
                    $s.downloadSVG(
                        {
                        nodes : $s.graph.nodes(),
                        edges : $s.graph.edges(),
                        }
                    )}
            );
        } catch (e) {};
    }
    else{
        try{
            var btn = document.getElementById("download_svg" + $n);
            btn.parentNode.removeChild(btn);
        } catch(e){};
    }
    if(all_download_state.includes('download_png')){
        //download png
        try {
            document.getElementById("download_png" + $n).addEventListener("click", function() {
                $s.renderers[0].snapshot({
                    format: 'png',
                    background: 'white',
                    labels: true,
                    download: true,
                    filename: 'graph.png'
                });

            });
        } catch (e) {};
    }
    else{
        try{
            var btn = document.getElementById("download_png" + $n);
            btn.parentNode.removeChild(btn);
        } catch(e){};
    }
    if(all_download_state.includes('download_adj')){
        try {
            document.getElementById("download_adj" + $n).addEventListener("click", function() {


                // Create items array
                var legend = Object.keys(map$n).map(function(key) {
                    return [key, map$n[key]];
                });

                // Sort the array based on the second element
                legend.sort(function(first, second) {
                    return first[1] - second[1];
                });

                var adj_str = "  ";
                for(i=0;i<adj$n.length;i++){
                    var k=0;
                    for(;k<max_label_length$n-legend[i][0].length || max_label_length$n-legend[i][0].length<0;k++){
                        adj_str+=" ";
                    }
                    adj_str+=legend[i][0]+" ";
                }

                adj_str+="\r\n";
                for(i=0;i<adj$n.length;i++){
                    var line = adj$n[i];

                    adj_str+=legend[i][0]+" ";

                    for(j=0;j<line.length;j++){

                        var k = 0;
                        if(line[j]){
                            for(;k<max_label_length$n-line[j].length || max_label_length$n-line[j].length<0;k++){
                                adj_str+=" ";
                            }
                            adj_str+=line[j]+" ";
                        }else{
                            for(;k<max_label_length$n-1 || max_label_length$n-1<0;k++){
                                adj_str+=" ";
                            }
                            adj_str+="0 ";
                        }
                    }
                    adj_str+="\r\n";
                }

                var element = document.createElement('a');
                element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(adj_str));
                element.setAttribute('download', "adjmatrix.txt");

                element.style.display = 'none';
                document.body.appendChild(element);

                element.click();

                document.body.removeChild(element);

            });
        } catch (e) {};
    }
    else{
        try{
            var btn = document.getElementById("download_png" + $n);
            btn.parentNode.removeChild(btn);
        } catch(e){};
    }
}
//the buttons related to the editweight_state
if(states$n.includes('editweight')){
    if(editweight_state.includes('editweight')){
        try{
            var btn = document.getElementById("changeW"+$n);

            // When the user clicks the button, open the modal
            btn.onclick = function() {

                set_one = false
                set_two = false
                unselect_set = false
                source = false
                target = false
                directed = false
                changeW$n=true;
            }


        }catch(e){};
    }else{
        try{
            var btn = document.getElementById("changeW"+$n);
            btn.parentNode.removeChild(btn);
        }catch(e){};
    }

}
//the buttons related to the multiple_drag_state
if(states$n.includes('multiple_drag')){
    if(multiple_drag_state.includes('drag')){
        try {
            document.getElementById("btn_multiple_sel" + $n).addEventListener("click", function() {
                multiple_sel = !multiple_sel;
            });
        } catch (e) {};
    }else{
        try{
            var btn = document.getElementById("btn_multiple_sel" + $n);
            btn.parentNode.removeChild(btn);
        }catch(e){};
    }
}
//SUBMIT Exercise
//al momento del submit creo json relativi al dizionario contenente le modifiche (graphN) e quello relativo al dizionorario per il render
// del grafo in sigma js
try {
    document.getElementById("save" + $n).addEventListener("click", function() {
        document.getElementById("save" + $n).style.backgroundColor = "#66cc66"
        var ts= new Date()
        var ts_s = ts.toLocaleString()
        var time_s = ts_s.replace(/[^A-Z0-9]/ig, "-");
        var image = $s.renderers[0].snapshot({
          format: 'png',
          background: 'white',
          labels: true,
        });

        console.log(image);

        set_one = false
        set_two = false
        unselect_set = false
        remove_edge = false;
        remove_node = false;
        changeW$n = false
        var fullgraph = {
            nodes: $s.graph.nodes(),
            edges: $s.graph.edges()
        }
        var graph_s = JSON.stringify(fullgraph);

        var command = `
textfile = open('allegati/ck_points/graph_data_`+$n+`_` + time_s + `.json', 'w')
textfile.write("""` + graph_s + `""")
textfile.close()
`;

        var png_command = `
img = """` + image + `"""
import re
import base64
to_rend = re.sub('^data:image/.+;base64,', '', img)
png = open('allegati/png_`+$n+`_` + time_s + `.png', 'wb')
byte_data = base64.b64decode(to_rend)
png.write(byte_data)
png.close()
`;

        kernel.execute(command)
        kernel.execute(png_command)
		alert("Salvato nella cartella 'allegati' ")
    });
} catch (e) {};