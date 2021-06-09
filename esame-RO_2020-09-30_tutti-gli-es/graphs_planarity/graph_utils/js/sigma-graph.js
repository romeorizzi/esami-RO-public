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
var scope$n = $scope;

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
    }
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

/////////////////////////////////////////CLICK EVENT\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

$s.bind('clickNode', function(e) {
    var node = e.data.node;
    var nodeId = node.id
    if (target && directed) {
        var new_edge_id = "e_a_" + source_id + "" + nodeId
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
        $s.refresh()
        source_id = null
        target_id = null
        target = false
        directed = false
    }
    if (target) {
        var new_edge_id = "e_a_" + source_id + "" + nodeId
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
        $s.refresh()
        source_id = null
        target_id = null
        target = false
    } else if (source) {
        source_id = nodeId
        source = false
        target = true
    } else if (remove_node) {
        for (n in dict_nf) {
            if (n == nodeId) {
                for (f of new Set(dict_nf[n])) {
                    var true_node = $s.graph.nodes(f)
                    try {
                        if (true_node.piece) {
                            $s.graph.dropNode(f)
                        }
                    } catch {
                        continue
                    }
                }
            }
        }
        $s.graph.dropNode(nodeId)
        $s.refresh()
        remove_node = false
        return
    } else if (set_one) {
        node.color = current_color;
        $s.refresh()
    } else if (set_two) {
        node.color = current_color;
        $s.refresh()
    } else if (unselect_set) {
        node.color = current_color;
        $s.refresh()
    }
});

var to_drop = []

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
    } else if (set_one) {
        for (key in dict_ef) {
            if (key == edgeId) {
                for (f of dict_ef[key]) {
                    var e = $s.graph.edges(f)
                    e.color = current_color
                    var source = $s.graph.nodes(e.source)
                    var target = $s.graph.nodes(e.target)
                    if (source.piece) {
                        source.color = current_color
                    }
                    if (target.piece) {
                        target.color = current_color
                    }
                }
            }
        }
        edge.color = current_color;
        $s.refresh()
    } else if (set_two) {
        for (key in dict_ef) {
            if (key == edgeId) {
                for (f of dict_ef[key]) {
                    var e = $s.graph.edges(f)
                    e.color = current_color
                    var source = $s.graph.nodes(e.source)
                    var target = $s.graph.nodes(e.target)
                    if (source.piece) {
                        source.color = current_color
                    }
                    if (target.piece) {
                        target.color = current_color
                    }
                }
            }
        }
        edge.color = current_color;
        $s.refresh()
    } else if (unselect_set) {
        for (key in dict_ef) {
            if (key == edgeId) {
                for (f of dict_ef[key]) {
                    var e = $s.graph.edges(f)
                    e.color = default_color_edge
                    var source = $s.graph.nodes(e.source)
                    var target = $s.graph.nodes(e.target)
                    if (source.piece) {
                        source.color = default_color_edge
                    }
                    if (target.piece) {
                        target.color = default_color_edge
                    }
                }
            }
        }
        edge.color = default_color_edge;
        $s.refresh()
    } /*else if (set_weight) {
        change_label(edge)
        $s.refresh()
    }*/
});


$s.bind('clickEdge', function(event) {
    if(!changeW$n){

        return;
    }

    var edge = event.data.edge;

    //si modificano solo gli archi con il peso
    if(!edge.label){
        return;
    }

    var source = "S";
    var target = "G";
    var type = "line";
    var weight = 0;
    if(edge.source in map$n && edge.target in map$n){
        source = edge.source;
        target = edge.target;
        weight = adj$n[map$n[edge.source]][map$n[edge.target]];
        type = edge.type;
    }else{
        //hidden nodes
        var list = dict_nf[edge.source];
        source = list[0];
        target = list[list.length-1];
        weight = adj$n[map$n[source]][map$n[target]];
        //if(source === list[list.length/2]){
        //alert(adj$n[map$n[target]][map$n[source]])
        if(adj$n[map$n[target]][map$n[source]] == null){
            type = "arrow";
        }
    }

    var lr = document.getElementById("lr"+$n);
    var lrLbl = document.getElementById("lrLbl"+$n);
    lr.value = source + " -> " + target;
    lrLbl.innerHTML = lr.value;
    lr.checked = true;
    lr.disabled = false;
    var rl = document.getElementById("rl"+$n);
    var rlLbl = document.getElementById("rlLbl"+$n);
    rl.value = target + " -> " + source;
    rlLbl.innerHTML = rl.value;
    if(type === "arrow"){

        rl.disabled = true;
    }else{
        rl.disabled = false;
    }

    // Get the modal
    var modal = document.getElementById("myModal"+$n);
    var span = document.getElementById("close"+$n);
    modal.style.display = "block";
    
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    //clear text
    var textField = document.getElementById("value"+$n);
    textField.value = ""+weight;

    //add confirm funct
    var confirmBtn = document.getElementById("cnf"+$n);
    confirmBtn.onclick = function() {
        
        var new_weight = parseInt(textField.value)
        if (! (new_weight != null && new_weight > 0 && new_weight <= weight)) {
        
            alert("Inserisci un numero tra 0 e " + weight);
            return;
        }

        if(lr.checked ){
            edge.label = "(" + lr.value+ ","+new_weight+")/"+weight;
        }else if(rl.checked){
            edge.label = "(" + rl.value+ ","+new_weight+")/"+weight;

        }else{
            alert("Seleziona la direzione del flusso");
            return;
        }
        $s.refresh();
        modal.style.display = "none";
    };

    return;
});


var adj$n;
var map$n;
var hidden_type$n={};
var max_label_length$n = 1;
buildAdj();

function buildAdj(){
    //assign node value from 0 to 1
    var nodes = $s.graph.nodes();
        
    map$n = {};
    
    var n_nodes=0;
    var i=0;
    for(; i < nodes.length; i++){
        if(!nodes[i].label){
            continue;
        }
        
        n_nodes++;
    }
    
    adj$n = new Array(n_nodes);
    i = 0;
    var j = 0;
    for(; i < nodes.length; i++){
        if(!nodes[i].label){
            continue;
        }
        
        map$n[nodes[i].id] = j;
        adj$n[j] = new Array(n_nodes);
        j++;
    }
    
    
    var edges = $s.graph.edges();
    
    //hidden edge type arrow/line
    var weigthed_graph = false;
    for(i=0; i < edges.length; i++){
        var edge = edges[i];
        
        if(edge.label){
            weigthed_graph=true;
        }

        //end segment
        if(!(edge.source in map$n) && edge.target in map$n){
           
            var type = edge.type;
            var list = dict_nf[edge.source];
            
            for(j=0;j<list.length;j++){
                
                if(list[j].includes("hidden")){
                    hidden_type$n[list[j]]=type;
                }
            }
        }
    }
    
    //building adj matrix
    i = 0;
    for(; i < edges.length; i++){
       
        var edge = edges[i];
        var label = edge.label;
            
        if(weigthed_graph){
            if(!label){
                continue;
            }
        }else{
            //To keep only the last segment on broken edge
            if(!label && !(edge.target in map$n)){
                continue;
            }
        }
        
        if(!label){
            label="1";
        }
        
        if(label.length>max_label_length$n){
            max_label_length$n=label.length;
        }
        
        if(edge.source in map$n && edge.target in map$n){
            
            
            adj$n[map$n[edge.source]][map$n[edge.target]] = label;
            if(edge.type === "line"){
                adj$n[map$n[edge.target]][map$n[edge.source]] = label;
            }
        }else{
            //hidden nodes
            var list = dict_nf[edge.source];
            var source = list[0];
            var target = list[list.length-1];
            adj$n[map$n[source]][map$n[target]] = label;
            //if(source === list[list.length/2]){
            if(hidden_type$n[edge.source] === "line"){
                adj$n[map$n[target]][map$n[source]] = label;
            }
        }
    }
}

/*function change_label(edge) {
    var new_weight = prompt("Enter new weight", "1");
    new_weight = parseInt(new_weight)
    if (new_weight != null && new_weight > 0) {
        edge.weight = "" + new_weight;
        edge.label = edge.label + "/" + new_weight
    } else {
        new_weight = edge.weight

        ("Bad value!");
    }
}*/

/*try {
    //set weight
    document.getElementById("btn_set_weight" + $n).addEventListener("click", function() {
        set_one = false
        remove_edge = false
        set_two = false
        unselect_set = false
        source = false
        target = false
        set_weight = true

    });
} catch (e) {};*/


try {
    //add edge
    document.getElementById("btn_add_e" + $n).addEventListener("click", function() {
        set_one = false
        set_two = false
        unselect_set = false
        source = true
        target = false
        changeW$n = false
    });
} catch (e) {};


try {
    //add edge
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


try {
    //yes choice
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

try {
    //remove node
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

if(scope$n.includes('color')){
    try {
        //selezione colori
        document.getElementById("btn_set_one" + $n).style.backgroundColor = color_first_set
        document.getElementById("btn_set_one" + $n).addEventListener("click", function() {
            set_two = false
            unselect_set = false
            set_one = true
            remove_node = false;
            remove_edge = false;
            changeW$n = false
            current_color = color_first_set
        });
        var for_bg = document.getElementById("btn_set_two" + $n);
        for_bg.style.backgroundColor = color_second_set;
        for_bg.style.color = "black";
        document.getElementById("btn_set_two" + $n).addEventListener("click", function() {
            set_one = false
            set_two = true
            changeW$n = false
            unselect_set = false
            remove_edge = false;
            remove_node = false;
            current_color = color_second_set
        });

        var for_bg = document.getElementById("btn_unselect_set" + $n);
        for_bg.style.backgroundColor = default_color_node;
        document.getElementById("btn_unselect_set" + $n).addEventListener("click", function() {
            set_one = false
            set_two = false
            unselect_set = false
            source = true
            target = false
            directed = true
            current_color = default_color_node;
        });
    } catch (e) {};
}else{
    try{
        var btn = document.getElementById("btn_set_one" + $n);
        btn.parentNode.removeChild(btn);

        btn = document.getElementById("btn_set_two" + $n);
        btn.parentNode.removeChild(btn);

        btn = document.getElementById("btn_unselect_set" + $n);
        btn.parentNode.removeChild(btn);
    }catch(e){};

}

if(scope$n.includes('drag')){
    //multiple sel
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

if(scope$n.includes('download')){
    //download svg
    try {
        document.getElementById("download_svg" + $n).addEventListener("click", function() {
            
            var nodes = $s.graph.nodes();
            var edges = $s.graph.edges();
            var map = {};
            
            var min_x;
            var min_y;
            var max_x;
            var max_y;

            var i = 0;
            for(;i< nodes.length; i++){
                map[nodes[i].id]=nodes[i];
                
                if(!min_x || nodes[i].x < min_x){
                    min_x = nodes[i].x;
                }

                if(!min_y || nodes[i].y < min_y){
                    min_y = nodes[i].y;
                }

                if(!max_x || nodes[i].x > max_x){
                    max_x = nodes[i].x;
                }

                if(!max_y || nodes[i].y > max_y){
                    max_y = nodes[i].y;
                }
            }

            max_x= max_x-min_x+60;
            max_y= max_y-min_y+60;
            
            var svg_namespace = "http://www.w3.org/2000/svg";
            
            var preface = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n';
            var svg = document.createElementNS(svg_namespace, "svg");
            svg.setAttribute("xmlns", svg_namespace);
            svg.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
            svg.setAttribute("version", "1.1");
            svg.setAttribute("width", max_x+"px");
            svg.setAttribute("height", max_y+"px");
            svg.setAttribute("x", "0px");
            svg.setAttribute("y", "0px");
            
            
            var defs = document.createElementNS(svg_namespace, "defs");
            svg.appendChild(defs);
            
            var marker = document.createElementNS(svg_namespace, "marker");
            marker.setAttribute("id", "arrowhead_gray");
            marker.setAttribute("fill", "#828282");
            marker.setAttribute("markerWidth", "3");
            marker.setAttribute("markerHeight", "3");
            marker.setAttribute("refX", "3");
            marker.setAttribute("refY", "1.5");
            marker.setAttribute("orient", "auto");
            defs.appendChild(marker);
            
            var polygon = document.createElementNS(svg_namespace, "polygon");
            polygon.setAttribute("points", "0 0, 3 1.5, 0 3");
            marker.appendChild(polygon);
            
            marker = document.createElementNS(svg_namespace, "marker");
            marker.setAttribute("id", "arrowhead_red");
            marker.setAttribute("fill", "#FF5722");
            marker.setAttribute("markerWidth", "3");
            marker.setAttribute("markerHeight", "3");
            marker.setAttribute("refX", "3");
            marker.setAttribute("refY", "1.5");
            marker.setAttribute("orient", "auto");
            defs.appendChild(marker);
            
            polygon = document.createElementNS(svg_namespace, "polygon");
            polygon.setAttribute("points", "0 0, 3 1.5, 0 3");
            marker.appendChild(polygon);
            
            marker = document.createElementNS(svg_namespace, "marker");
            marker.setAttribute("id", "arrowhead_yellow");
            marker.setAttribute("fill", "#FFD600");
            marker.setAttribute("markerWidth", "3");
            marker.setAttribute("markerHeight", "3");
            marker.setAttribute("refX", "3");
            marker.setAttribute("refY", "1.5");
            marker.setAttribute("orient", "auto");
            defs.appendChild(marker);
            
            polygon = document.createElementNS(svg_namespace, "polygon");
            polygon.setAttribute("points", "0 0, 3 1.5, 0 3");
            marker.appendChild(polygon);
            
            var g_edge = document.createElementNS(svg_namespace, "g");
            svg.appendChild(g_edge);
            
            var g_nodes = document.createElementNS(svg_namespace, "g");
            svg.appendChild(g_nodes);
            
            var g_label = document.createElementNS(svg_namespace, "g");
            svg.appendChild(g_label);
            
            for(i=0;i<nodes.length;i++){
                var node = document.createElementNS(svg_namespace, 'circle');
                var x = nodes[i].x-min_x+30;
                var y = nodes[i].y-min_y+30;
                
                if(nodes[i].label){
                    node.setAttributeNS(null, 'data-node-id', nodes[i].id);
                    
                    var label = document.createElementNS(svg_namespace, 'text');
                    label.setAttribute("data-label-target", nodes[i].id);
                    label.setAttribute("font-size", "17");
                    label.setAttribute("font-family", "arial");
                    label.setAttribute("x", (x+7)+"");
                    label.setAttribute("y", (y+7)+"");
                    label.setAttribute("fill", "#000");
                    label.textContent = nodes[i].label;
                    g_label.appendChild(label);
                }
                node.setAttributeNS(null, 'cx', x);
                node.setAttributeNS(null, 'cy', y);
                node.setAttributeNS(null, 'r', "3");
                node.setAttributeNS(null, 'fill', nodes[i].color);
                g_nodes.appendChild(node);
            }
            
            for(i=0;i<edges.length;i++){
                var edge = document.createElementNS(svg_namespace, 'line');
                var source = map[edges[i].source];
                var target = map[edges[i].target];
                
                var source_x = source.x-min_x+30;
                var source_y = source.y-min_y+30;
                var target_x = target.x-min_x+30;
                var target_y = target.y-min_y+30;
                
                //set line param
                edge.setAttribute("data-edge-id", edges[i].id);
                edge.setAttribute("stroke-width", "3");
                var color = edges[i].color;
                edge.setAttribute("stroke", color);
                edge.setAttribute("x1", source_x+"");
                edge.setAttribute("y1", source_y+"");
                edge.setAttribute("x2", target_x+"");
                edge.setAttribute("y2", target_y+"");
                
                if(edges[i].type === "arrow"){
                    var arrowhead;
                    if(color === "#828282"){
                        arrowhead="url(#arrowhead_gray)";
                    }else if(color === "#FF5722"){
                        arrowhead="url(#arrowhead_red)";
                    }else{
                        arrowhead="url(#arrowhead_yellow)";
                    
                    }
                    edge.setAttribute("marker-end", arrowhead);
                }
                
                if(edges[i].weight){
                    //var angle = Math.atan2(Math.abs(target_y - source_y), Math.abs(target_x - source_x)) * 180 / Math.PI;
                    
                    var label = document.createElementNS(svg_namespace, 'text');
                    label.setAttribute("data-label-target", edges[i].id);
                    label.setAttribute("font-size", "17");
                    label.setAttribute("font-family", "arial");
                    label.setAttribute("text-anchor", "middle");
                    label.setAttribute("x", (((source_x+target_x)/2)+7)+"");
                    label.setAttribute("y", (((source_y+target_y)/2)+7)+"");
                    label.setAttribute("fill", "#000");
                    //label.setAttribute("transform", "rotate("+angle+", "+(((source_x+target_x)/2)+7)+","+(((source_y+target_y)/2)+7)+")");
                    label.textContent = edges[i].weight;
                    g_label.appendChild(label);
                }
                
                g_edge.appendChild(edge);
            }
            
            var svgString = svg.outerHTML
            var svgBlob = new Blob([preface,svgString], {type:"image/svg+xml;charset=utf-8"});
            var svgUrl = URL.createObjectURL(svgBlob);
            var downloadLink = document.createElement("a");
            downloadLink.href = svgUrl;
            downloadLink.download = "graph.svg";
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            
        });
    } catch (e) {};

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

    //download adj matrix
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
}else{
    try{
        var btn = document.getElementById("download_svg" + $n);
        btn.parentNode.removeChild(btn);

        btn = document.getElementById("download_png" + $n);
        btn.parentNode.removeChild(btn);

        btn = document.getElementById("download_adj" + $n);
        btn.parentNode.removeChild(btn);
    }catch(e){};
}

if(scope$n.includes('editweight')){
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
