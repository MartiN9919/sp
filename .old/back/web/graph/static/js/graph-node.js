class GRAPH_NODE {



// ***********************************************
// TEST
// ***********************************************
node_test_action = function(menu_item, data, sender, point){
    this.data_nodes.push(
        {
            [GRAPH_SVG.KEY_NODE_OBJ_ID]: 5,
            [GRAPH_SVG.KEY_NODE_REC_ID]: 110,
            [GRAPH_SVG.KEY_NODE_LABEL]:  'Семен Семенович',
            [GRAPH_SVG.KEY_NODE_MARK]:   true,
            id: '5_110',
            'x': point[0],
            'y': point[1],
        }, {
            [GRAPH_SVG.KEY_NODE_OBJ_ID]: 6,
            [GRAPH_SVG.KEY_NODE_REC_ID]: 111,
            [GRAPH_SVG.KEY_NODE_LABEL]:  'ГП "Тортилла & Со"',
            [GRAPH_SVG.KEY_NODE_MARK]:   false,
            id: '6_111',
            'x': point[0]+50,
            'y': point[1]+50,
        },
    );

    this.data_links.push(
        {
            [GRAPH_SVG.KEY_LINK_NODES]:    [{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 102},{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 110}],
            [GRAPH_SVG.KEY_LINK_KEY_ID]:   100,
            [GRAPH_SVG.KEY_LINK_KEY_DATE]: '2020-01-06',
            [GRAPH_SVG.KEY_LINK_GROUP_ID]: 1,
            source: '5_102',
            target: '5_110',
        }, {
            [GRAPH_SVG.KEY_LINK_NODES]:    [{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 110},{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 6, [GRAPH_SVG.KEY_NODE_REC_ID]: 111}],
            [GRAPH_SVG.KEY_LINK_KEY_ID]:   105,
            [GRAPH_SVG.KEY_LINK_KEY_DATE]: '2020-01-14',
            [GRAPH_SVG.KEY_LINK_GROUP_ID]: 2,
            source: '5_110',
            target: '6_111',
        }, {
            [GRAPH_SVG.KEY_LINK_NODES]:    [{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 110},{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 100}],
            [GRAPH_SVG.KEY_LINK_KEY_ID]:   105,
            [GRAPH_SVG.KEY_LINK_KEY_DATE]: '2020-01-14',
            [GRAPH_SVG.KEY_LINK_GROUP_ID]: 2,
            source: '5_110',
            target: '5_100',
        },
    );
    //this.data_nodes.splice(4, 3);
    this.data_update();
};



// ***********************************************
// ADD / DEL
// ***********************************************
node_add_menu = function(menu_item, data, sender, point){
    let obj_data = menu_item.data;
    let inp_id   = new FORM_EL_ID({
        'obj_data':  obj_data,
        'cb_action': function(data_id){
            console.log(data_id);
            setTimeout(function() {
                inp_id.free();
                inp_id = undefined;
                //if (data_id.id==0) this.org_get_name(obj_data, data_id);
            }.bind(this), 10);
        }.bind(this),
    });
};

node_del_menu = function(menu_item, data, sender, point){
    let i;
    for (i = this.data_links.length; i--;) {                        // удалить связи с удаляемым узлом
        if ((this.data_links[i].source.id == data.id) || (this.data_links[i].target.id == data.id)) {
            this.data_links.splice(i, 1);
        }
    }
    this.data_nodes.splice(data.index, 1);                          // удалить item в data_nodes

    i=0; this.data_links.forEach(d => d.index = i++);               // проставить заново индексы в data_links
    i=0; this.data_nodes.forEach(d => d.index = i++);               // проставить заново индексы в data_nodes
    this.data_update();
};

node_delall_menu = function(menu_item, data, sender, point) {
    this.data_nodes = [];
    this.data_links = [];
    this.data_update(0);
};

// ДОСТУПНОСТЬ ОЧИСТКИ ХОЛСТА: ЕСТЬ ХОТЬ ОДИН УЗЕЛ
node_delall_enabled = function() {
    return (this.data_nodes.length>0);
};



// ***********************************************
// УСТАНОВИТЬ / СНЯТЬ ОТМЕТКУ
// ***********************************************
node_mark_toggle_event = function(e, d) { this.node_mark_toggle_menu(undefined, d); }
node_mark_toggle_menu  = function(menu_item, data, sender, point) {
    data.mark = !(data.mark||false);
    this.data_update(0);
};

// СНЯТЬ ВСЕ ОТМЕТКИ
node_mark_clearall_menu = function(menu_item, data, sender, point) {
    this.data_nodes.forEach(d => d.mark=false);
    this.data_update(0);
};

// ДОСТУПНОСТЬ СНЯТИЯ ОТМЕТКИ: ИМЕЕТ ХОТЬ ОДИН УЗЕЛ ОТМЕТКУ
node_mark_clearall_enabled = function() {
    let enabled = false;
    this.data_nodes.forEach(d => enabled = enabled || (d.mark||false));
    return enabled;
};




// ***********************************************
// ОТКРЕПИТЬ
// ***********************************************
node_pin_clear_event = function(e, d) { this.node_pin_clear_menu(undefined, d); };
node_pin_clear_menu  = function(menu_item, data, svg) {
    data.fx=null; data.fy=null;
    this.data_update();
};

node_pin_clearall_menu = function(menu_item, data, svg) {
    this.data_nodes.forEach(d => { d.fx=null; d.fy=null; });
    this.data_update();
};

// ДОСТУПНОСТЬ ОТКРЕПЛЕНИЯ: ИМЕЕТ ЛИ УЗЕЛ ЗАКРЕПЛЕНИЕ
node_pin_clear_enabled = function(data) {
    return (('fx' in data) && (data.fx!=null));
};

node_pin_clearall_enabled = function(data) {
    let enabled = false;
    this.data_nodes.forEach(d => enabled = enabled || (('fx' in d) && (d.fx!=null)));
    return enabled;
};





// ***********************************************
// УЗЕЛ НА ПЕРЕДНИЙ ПЛАН
// ***********************************************
node_mouse_over_event = function(e, d) {
    if (!d3.select(e.target).classed(GRAPH_SVG.CL_NODE_MAIN)) return;   // не реагировать ни на что, кроме основного элемента

    let node_d3 = d3.select('#g_'+d.id);                                // d3.select(e.target) недопустимо, т.к. меняем this.data_nodes

    node_d3.moveToFront();                                              // перенести g в структуре DOM
    this.data_nodes.push(this.data_nodes.splice(d.index, 1)[0]);        // перенести item в data_nodes
    let i=0; this.data_nodes.forEach(d => d.index = i++);               // проставить заново индексы в data_nodes

    let node_data = node_d3.datum();                                    // прозрачность узлов
    this.NODES_D3                      .transition().duration(GRAPH_SVG.FADE_ON).style('opacity', d2 => this.data_neigh(node_data.id, d2.id)?undefined:0.1);
    this.NODES_D3  .selectAll('.label').transition().duration(GRAPH_SVG.FADE_ON).style('opacity', d2 => this.data_neigh(node_data.id, d2.id)?undefined:0);
    this.G_LINKS_D3.selectAll('.link') .transition().duration(GRAPH_SVG.FADE_ON).style('opacity', d2 => ((d2.source.id==node_data.id)||(d2.target.id==node_data.id))?undefined:0.1);
};

node_mouse_out_event = function(e, d) {
    this.NODES_D3                      .transition().duration(GRAPH_SVG.FADE_OFF).style('opacity', undefined);
    this.NODES_D3  .selectAll('.label').transition().duration(GRAPH_SVG.FADE_OFF).style('opacity', undefined);
    this.G_LINKS_D3.selectAll('.link') .transition().duration(GRAPH_SVG.FADE_OFF).style('opacity', undefined);
};




// ***********************************************
// id узла
// ***********************************************
node_id = (obj_id, rec_id) => obj_id+'-'+rec_id;

}
