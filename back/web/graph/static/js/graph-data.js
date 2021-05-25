class GRAPH_DATA {

// ***********************************************
// INI
// ***********************************************
data_ini = function(){
    this.SIMULATION = d3.forceSimulation()
        .force('charge_force', d3.forceManyBody().strength(-600))
        .force('center_force', d3.forceCenter(this.PARENT_JS.clientWidth/2, this.PARENT_JS.clientHeight/2))
        .on   ('tick',         this.graph_tick);
    this.G_MAIN_D3  = this.SVG_D3   .append('g').attr('class', 'graph-root').attr('class', 'select_off');
    this.G_LINKS_D3 = this.G_MAIN_D3.append('g').attr('class', 'links');
};


// ***********************************************
// UPDATE
// ***********************************************
data_update = function(alpha=0.1){
    function vis_node_color(d){ return (d[GRAPH_SVG.KEY_NODE_OBJ_ID]   == 5)?'blue':'pink'; }
    function vis_link_color(d){ return (d[GRAPH_SVG.KEY_LINK_GROUP_ID] == 1)?'green':'red'; }
    function vis_node_text (d){ return  d[GRAPH_SVG.KEY_NODE_LABEL]; }

    this.SIMULATION.stop();

    this.LINKS_D3 = this.G_LINKS_D3.selectAll('.link').data(this.data_links).join(
        function(enter){
            let links_enter = enter.append('line')
                .attr('class', 'link')
                .style('stroke', vis_link_color);
                //.join('.link');
                //.merge(this.LINKS_D3);
        }.bind(this),
        function(update){
            return update;
        }.bind(this),
        function(exit){
            return exit.remove();
        }.bind(this)
    );

    this.NODES_D3 = this.G_MAIN_D3.selectAll('.node').data(this.data_nodes).join(
        function(enter){
            let nodes_enter = enter.append('g')
                .attr('id', d => 'g_'+d[GRAPH_SVG.KEY_NODE_OBJ_ID]+'_'+d[GRAPH_SVG.KEY_NODE_REC_ID])    // нужно для перемещения на передний план
                .attr('class', 'node')
                //.classed('marked', d => d.mark || false)
                .on('click', function(e, d){
                    console.log('click');
                    if (e.shiftKey){ this.node_mark_toggle_event(e, d); }
                }.bind(this))
                .on('dblclick',  this.node_pin_clear_event)
                .on("mouseover", this.node_mouse_over_event)
                .on("mouseout",  this.node_mouse_out_event)
                .call(this.graph_node_drag)
                .call(this.menu_node_ini);
            nodes_enter.append('svg:circle')
                .attr('class', GRAPH_SVG.CL_NODE_MAIN)
                .attr('r', 5)
                .attr('fill', vis_node_color)
                .attr('opacity', 0.5)
                .style('filter', 'url(#def-shadow-1)')
                .transition()
                .duration(300)
                .attr('opacity', 1.0)
                .attr('r', 10);
            nodes_enter.append('svg:text')
                .attr('class', 'label')
                .style('filter', 'url(#def-shine-2)')
                .attr('y', 16+8)
                .attr('dy', '.35em')
                .text(vis_node_text);
            nodes_enter.append('svg:path')
                .attr('class', 'mark')
                .style('filter', 'url(#def-shadow-0)')
                .style('display', d => (d.mark||false)?undefined:'none')
                .attr('d', 'M 16.000 -10.000 L 23.053 -6.292 L 21.706 -14.146 L 27.413 -19.708 L 19.527 -20.854 L 16.000 -28.000 L 12.473 -20.854 L 4.587 -19.708 L 10.294 -14.146 L 8.947 -6.292 L 16.000 -10.000 L 23.053 -6.292');
            // nodes_enter.append('svg:image')
            //     .attr('xlink:href', function(d) { return d.icon; });
            return nodes_enter;
        }.bind(this),
        function(update){
            update.select('.mark')
                .style('display', d => (d[GRAPH_SVG.KEY_NODE_MARK]||false)?undefined:'none');
            return update;
        }.bind(this),
        function(exit){
            return exit.remove();                                           // .transition().duration(1000) not working
        }.bind(this)
    );

    this.NEIGHT = [];                                                       // список соседних узлов
    this.data_links.forEach(function(d) {
        this.NEIGHT[(d.source.id||d.source)+'-'+(d.target.id||d.target)]=true;
        this.NEIGHT[(d.target.id||d.target)+'-'+(d.source.id||d.source)]=true;
    }.bind(this));

    this.SIMULATION
        .nodes(this.data_nodes)
        .force('links', d3.forceLink(this.data_links).id( d => d.id ))      // идентификаторы nodes для построения links
        .alpha(alpha)                                                       // встряска
        // .alphaDecay(0.01)                                                // угасание
        .restart();
};


data_neigh = function(id_1, id_2) {
    return (id_1==id_2) || this.NEIGHT[id_1+'-'+id_2];
};




}

