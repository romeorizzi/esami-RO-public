;(function(undefined){
    'use strict';

    if (typeof sigma === 'undefined')
    throw 'sigma.renderers.snapshot: sigma not in scope.';

    sigma.prototype.buildVectSelect = function(params){

        var nodes = params.nodes;
        var map   = params.map;
        var n_nodes=0;
        var i=0;
        var j=0;
        var vect_nodes = new Array(n_nodes);
        //n_nodes are the nodes with a label (it don't count the hidden ones)
        for(;i<nodes.length;i++){
            // map[nodes[i].id] = j;
            if(!nodes[i].label){
                continue;
            }
            vect_nodes[j]  = new Array(map[nodes[j].id], 0);
            j++;
        }
        return [vect_nodes]
    }
///////////////////////////////////build Adjancy matrix \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    //buildAdj build the adjancy matrix (it is used from most of the function in sigma-graph.js)
    sigma.prototype.buildAdj = function(params){
        //parameter required in input --> supporting variable
        var nodes = params.nodes;
        var edges = params.edges;
        // var nodes = g.nodes
        // var edges = g.edges


        var hidden_type={};
        var max_label_length = 1;


        // general supporting variable
        var n_nodes=0;
        var i=0;

        var map = {};
        var adj = new Array(n_nodes);
        //build a copy of adj to change the values
        var change_adj = new Array(n_nodes);
        var select_adj = new Array(n_nodes);

        for(; i < nodes.length; i++){
            if(!nodes[i].label){
                continue;
            }

            n_nodes++;
        }


        i = 0;
        var j = 0;
        //build the map which contains the nodes label
        for(; i < nodes.length; i++){
            if(!nodes[i].label){
                continue;
            }

            map[nodes[i].id] = j;
            adj[j] = new Array(n_nodes);
            change_adj[j] = new Array(n_nodes);
            select_adj[j] = new Array(n_nodes);
            j++;
        }


        //hidden edge type arrow/line
        var weigthed_graph = false;
        for(i=0; i < edges.length; i++){
            var edge = edges[i];

            if(edge.label){
                weigthed_graph=true;
            }

            //end segment
            if(!(edge.source in map) && edge.target in map){

                var type = edge.type;
                var list = dict_nf[edge.source];

                for(j=0;j<list.length;j++){

                    if(list[j].includes("hidden")){
                        hidden_type[list[j]]=type;
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
                if(!label && !(edge.target in map)){
                    continue;
                }
            }

            if(!label){
                label="1";
            }

            if(label.length>max_label_length){
                max_label_length=label.length;
            }

            if(edge.source in map && edge.target in map){


                adj[map[edge.source]][map[edge.target]] = label;
                change_adj[map[edge.source]][map[edge.target]] = label;
                select_adj[map[edge.source]][map[edge.target]] = 0;
                if(edge.type === "line"){
                    adj[map[edge.target]][map[edge.source]] = label;
                    change_adj[map[edge.target]][map[edge.source]] = label;
                    select_adj[map[edge.target]][map[edge.source]] = 0;
                }
            }else{
                //hidden nodes
                var list = dict_nf[edge.source];
                var source = list[0];
                var target = list[list.length-1];
                adj[map[source]][map[target]] = label;
                change_adj[map[source]][map[target]] = label;
                select_adj[map[source]][map[target]] = 0;
                //if(source === list[list.length/2]){
                if(hidden_type[edge.source] === "line"){
                    adj[map[target]][map[source]] = label;
                    change_adj[map[target]][map[source]] = label;
                    select_adj[map[target]][map[source]] = 0;
                }
            }
        }
        return [adj, map, hidden_type, max_label_length, change_adj, select_adj];
    };

///////////////////////////////////changeWeightEdge\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    // FUNZIONANTE:
        // $s è passato come parametro
        // bisogna recuperarlo da sigma
    // changeWeightEdge is an utility function that allows you to set the weight of the edge flow
    sigma.prototype.changeWeightEdge = function(params){

        var changeW     = params.changeW;
        var adj         = params.adj;
        var map         = params.map;
        var n_var       = params.n_var;
        var edge        = params.edge;
        var s_var       = params.s_var;
        var changed_adj = params.matrixInit



        if(!changeW){
            return [changed_adj];
        }
        //si modificano solo gli archi con il peso
        if(!edge.label){
            return [changed_adj];
        }

        var source = "S";
        var target = "G";
        var type = "line";
        var weight = 0;
        if(edge.source in map && edge.target in map){
            source = edge.source;
            target = edge.target;
            weight = adj[map[edge.source]][map[edge.target]];
            type = edge.type;
        }else{
            //hidden nodes
            var list = dict_nf[edge.source];
            source = list[0];
            target = list[list.length-1];
            weight = adj[map[source]][map[target]];
            //if(source === list[list.length/2]){
            //alert(adj[map[target]][map[source]])
            if(adj[map[target]][map[source]] == null){
                type = "arrow";
            }
        }
        var lr = document.getElementById("lr"+n_var);
        var lrLbl = document.getElementById("lrLbl"+n_var);
        lr.value = source + " -> " + target;
        lrLbl.innerHTML = lr.value;
        lr.checked = true;
        lr.disabled = false;
        var rl = document.getElementById("rl"+n_var);
        var rlLbl = document.getElementById("rlLbl"+n_var);
        rl.value = target + " -> " + source;
        rlLbl.innerHTML = rl.value;
        if(type === "arrow"){

            rl.disabled = true;
        }else{
            rl.disabled = false;
        }

        // Get the modal
        var modal = document.getElementById("myModal"+n_var);
        var span = document.getElementById("close"+n_var);
        modal.style.display = "block";

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
            modal.style.display = "none";
        }

        //clear text
        var textField = document.getElementById("value"+n_var);
        textField.value = ""+weight;

        //add confirm funct
        var confirmBtn = document.getElementById("cnf"+n_var);
        confirmBtn.onclick = function() {

            var new_weight = parseInt(textField.value)
            //posso volere flusso 0?
            if (! (new_weight != null && new_weight > 0 && new_weight <= weight)) {

                alert("Inserisci un numero tra 0 e " + weight);
                return [changed_adj];
            }

            if(lr.checked ){
                edge.label = "(" + lr.value+ "),"+new_weight+"/"+weight;
                changed_adj[map[source]][map[target]] = "" + new_weight;
                changed_adj[map[target]][map[source]] = "" + 0;
            }else if(rl.checked){
                edge.label = "(" + rl.value+ "),"+new_weight+"/"+weight;
                changed_adj[map[target]][map[source]] = "" + new_weight;
                changed_adj[map[source]][map[target]] = "" + 0;


            }else{
                alert("Seleziona la direzione del flusso");
                return [changed_adj];
            }
            s_var.refresh();
            modal.style.display = "none";
        };
        //this matrix will return the changed values

        return [changed_adj];
    };

    sigma.prototype.downloadSVG = function(params){
        // var nodes = $s.graph.nodes();
        // var edges = $s.graph.edges();
        // var nodes = g.nodes;    //.nodes();
        // var edges = g.edges;
        var nodes = params.nodes;
        var edges = params.edges;


        var map = {}; //locale

        //locale
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

        // locale
        //preparing the head of the HTML
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


        //create a new element
        var defs = document.createElementNS(svg_namespace, "defs");
        svg.appendChild(defs);

        // create the arrow rappresentation
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

        // create the red arrow rappresentation
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

        // create the yellow arrow rappresentation
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
                // label.textContent = edges[i].weight;
                label.textContent = edges[i].label;
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
    };
}).call(this);
