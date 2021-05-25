'use strict';

$(document).ready(function(){
    // чтобы скрыть не отформатированный html
    $('body').css('display', 'block').trigger('resize');


    // выбор меню выделить
    $('#nav-graph').splitbutton('disable');


    let obj_graph_org = new class GRAPH_ORG {
        constructor() {
        this.ID_LAYOUT_CENTER   = 'layout-center';

    // BASE
    // $('#main')
    //     .css('width', '100%')
    //     .css('height', '100%')
    //     .append('<div id="graph" style="width: 100%; height: 100%;"></div>');
    // this.resize(undefined);

    // // LAYOUT
    // $('#graph')
    //     .layout({
    //         fit:      true,
    //         border:   false,
    //         width:    '100%',
    //         height:   '100%',
    //     })
    //     .layout('add', {
    //         id:       this.ID_LAYOUT_CENTER,
    //         region:   'center',
    //         border:   false,
    //         owerflow: 'hidden',
    //     });

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

    };


    }


})

