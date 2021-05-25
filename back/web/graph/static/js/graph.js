'use strict';


let obj_graph_org = new class GRAPH_ORG {
constructor() {
    this.ID_LAYOUT_CENTER   = 'layout_center';

    // ГЛАВНОЕ МЕНЮ
    topmenu_select('nav-graph');

    // BASE
    $('#main')
        .css('width', '100%')
        .css('height', '100%')
        .append('<div id="graph" style="width: 100%; height: 100%;"></div>');
    this.resize(undefined);

    // LAYOUT
    $('#graph')
        .layout({
            fit:      true,
            border:   false,
            width:    '100%',
            height:   '100%',
        })
        // .layout('add', {
        //     id:       this.id_layout_north,
        //     region:   'north',
        //     height:   '35px',
        //     border:   false,
        //     style: {
        //         'text-align': 'right',
        //         padding:      '0 0 5px 0',
        //     },
        // })
        .layout('add', {
            id:       this.ID_LAYOUT_CENTER,
            region:   'center',
            border:   false,
            owerflow: 'hidden',
        });

    // SVG
    let obj_graph_svg = new GRAPH_SVG(this.ID_LAYOUT_CENTER, {
        data_nodes: [
            {"name": "Lillian", "obj": "F", mark: true},
            {"name": "Gordon", "obj": "M", mark: true},
            {"name": "Sylvester", "obj": "M", mark: false},
        ],
        data_links: [
            {"source": "Lillian",   "target": "Gordon",    "type":"A" },
            {"source": "Lillian",   "target": "Sylvester", "type":"A" },
            {"source": "Sylvester", "target": "Gordon",    "type":"E"},
        ],
    });

    // EVENT: RESIZE
    window.addEventListener('resize', this.resize, false);
}


// ============================================================
// RESIZE
// ============================================================
resize = function(element) {
    let JS_body   = document.querySelector('body');
    let JS_main   = document.querySelector('#main');
    //let JS_center = document.querySelector('#main');
    JS_body.style.height = (document.documentElement.clientHeight - 1)+'px';
    JS_main.style.height = (document.documentElement.clientHeight - JS_main.offsetTop - 1)+'px';
}.bind(this);


}
