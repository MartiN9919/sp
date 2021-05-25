'use strict';

class GRAPH_SVG {
static KEY_NODE_REC_ID      = 'rec_id';
static KEY_NODE_OBJ_ID      = 'obj_id';
static KEY_NODE_LABEL       = 'label';
static KEY_NODE_ICON        = 'icon';            // устанавливать здесь пока
static KEY_NODE_MARK        = 'mark';            // устанавливать здесь пока

static KEY_LINK_NODES       = 'nodes';
static KEY_LINK_KEY_ID      = 'key_id';
static KEY_LINK_KEY_DATE    = 'key_date';
static KEY_LINK_GROUP_ID    = 'group_id';

static FADE_ON              = 200;               // время исчезновения, мс
static FADE_OАА             = 200;               // время появления, мс

static CL_NODE_MAIN         = 'node-main';

constructor(parent_id, options={}) {
    // работа классов в одном контексте this
    let graph_defs                  = new GRAPH_DEFS();
    this.defs_ini                   = graph_defs.defs_ini.bind(this);

    let graph_data                  = new GRAPH_DATA();
    this.data_ini                   = graph_data.data_ini.bind(this);
    this.data_update                = graph_data.data_update.bind(this);
    this.data_neigh                 = graph_data.data_neigh.bind(this);

    let graph_node                  = new GRAPH_NODE();
    this.node_test_action           = graph_node.node_test_action.bind(this);

    this.node_add_menu              = graph_node.node_add_menu.bind(this);
    this.node_del_menu              = graph_node.node_del_menu.bind(this);
    this.node_delall_menu           = graph_node.node_delall_menu.bind(this);
    this.node_delall_enabled        = graph_node.node_delall_enabled.bind(this);

    this.node_mark_toggle_event     = graph_node.node_mark_toggle_event.bind(this);
    this.node_mark_toggle_menu      = graph_node.node_mark_toggle_menu.bind(this);
    this.node_mark_clearall_menu    = graph_node.node_mark_clearall_menu.bind(this);
    this.node_mark_clearall_enabled = graph_node.node_mark_clearall_enabled.bind(this);

    this.node_pin_clear_event       = graph_node.node_pin_clear_event.bind(this);
    this.node_pin_clear_menu        = graph_node.node_pin_clear_menu.bind(this);
    this.node_pin_clearall_menu     = graph_node.node_pin_clearall_menu.bind(this);
    this.node_pin_clear_enabled     = graph_node.node_pin_clear_enabled.bind(this);
    this.node_pin_clearall_enabled  = graph_node.node_pin_clearall_enabled.bind(this);

    this.node_mouse_over_event      = graph_node.node_mouse_over_event.bind(this);
    this.node_mouse_out_event       = graph_node.node_mouse_out_event.bind(this);
    this.node_id                    = graph_node.node_id.bind(this);

    let graph_menu_main             = new GRAPH_MENU_MAIN();
    this.menu_main_ini              = graph_menu_main.menu_main_ini.bind(this);
    this.menu_main_help             = graph_menu_main.menu_main_help.bind(this);
    this.graph_key                  = graph_menu_main.graph_key.bind(this);

    let graph_menu_node             = new GRAPH_MENU_NODE();
    this.menu_node_ini              = graph_menu_node.menu_node_ini.bind(this);

    // this.data_nodes = options.data_nodes||[];   // [...array] - deep copy
    // this.data_links = options.data_links||[];

    this.data_nodes = [
        {
            [GRAPH_SVG.KEY_NODE_OBJ_ID]: 5,
            [GRAPH_SVG.KEY_NODE_REC_ID]: 100,
            [GRAPH_SVG.KEY_NODE_LABEL]:  'Иванов',
            [GRAPH_SVG.KEY_NODE_MARK]:   true,
            id: '5_100',
        }, {
            [GRAPH_SVG.KEY_NODE_OBJ_ID]: 5,
            [GRAPH_SVG.KEY_NODE_REC_ID]: 101,
            [GRAPH_SVG.KEY_NODE_LABEL]:  'Петров',
            [GRAPH_SVG.KEY_NODE_MARK]:   false,
            id: '5_101',
        }, {
            [GRAPH_SVG.KEY_NODE_OBJ_ID]: 5,
            [GRAPH_SVG.KEY_NODE_REC_ID]: 102,
            [GRAPH_SVG.KEY_NODE_LABEL]:  'Козлов',
            [GRAPH_SVG.KEY_NODE_MARK]:   false,
            id: '5_102',
        }, {
            [GRAPH_SVG.KEY_NODE_OBJ_ID]: 5,
            [GRAPH_SVG.KEY_NODE_REC_ID]: 103,
            [GRAPH_SVG.KEY_NODE_LABEL]:  'Чудаков',
            [GRAPH_SVG.KEY_NODE_MARK]:   false,
            id: '5_103',
        }, {
            [GRAPH_SVG.KEY_NODE_OBJ_ID]: 5,
            [GRAPH_SVG.KEY_NODE_REC_ID]: 104,
            [GRAPH_SVG.KEY_NODE_LABEL]:  'Белая',
            [GRAPH_SVG.KEY_NODE_MARK]:   false,
            id: '5_104',
        }, {
            [GRAPH_SVG.KEY_NODE_OBJ_ID]: 6,
            [GRAPH_SVG.KEY_NODE_REC_ID]: 100,
            [GRAPH_SVG.KEY_NODE_LABEL]:  'ООО "Рога и копыта"',
            [GRAPH_SVG.KEY_NODE_MARK]:   false,
            id: '6_100',
        }, {
            [GRAPH_SVG.KEY_NODE_OBJ_ID]: 6,
            [GRAPH_SVG.KEY_NODE_REC_ID]: 101,
            [GRAPH_SVG.KEY_NODE_LABEL]:  'УП "Страйк"',
            [GRAPH_SVG.KEY_NODE_MARK]:   false,
            id: '6_101',
        },
    ];
    this.data_links = [
        {
            [GRAPH_SVG.KEY_LINK_NODES]:    [{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 102},{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 103}],
            [GRAPH_SVG.KEY_LINK_KEY_ID]:   100,
            [GRAPH_SVG.KEY_LINK_KEY_DATE]: '2020-01-05',
            [GRAPH_SVG.KEY_LINK_GROUP_ID]: 1,
            source: '5_102',
            target: '5_103',
        }, {
            [GRAPH_SVG.KEY_LINK_NODES]:    [{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 100},{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 101}],
            [GRAPH_SVG.KEY_LINK_KEY_ID]:   100,
            [GRAPH_SVG.KEY_LINK_KEY_DATE]: '2020-01-01',
            [GRAPH_SVG.KEY_LINK_GROUP_ID]: 1,
            source: '5_100',
            target: '5_101',
        }, {
            [GRAPH_SVG.KEY_LINK_NODES]:    [{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 100},{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 6, [GRAPH_SVG.KEY_NODE_REC_ID]: 100}],
            [GRAPH_SVG.KEY_LINK_KEY_ID]:   101,
            [GRAPH_SVG.KEY_LINK_KEY_DATE]: '2020-01-02',
            [GRAPH_SVG.KEY_LINK_GROUP_ID]: 2,
            source: '5_100',
            target: '6_100',
        }, {
            [GRAPH_SVG.KEY_LINK_NODES]:    [{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 100},{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 6, [GRAPH_SVG.KEY_NODE_REC_ID]: 101}],
            [GRAPH_SVG.KEY_LINK_KEY_ID]:   105,
            [GRAPH_SVG.KEY_LINK_KEY_DATE]: '2020-01-03',
            [GRAPH_SVG.KEY_LINK_GROUP_ID]: 2,
            source: '5_100',
            target: '6_101',
        }, {
            [GRAPH_SVG.KEY_LINK_NODES]:    [{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 5, [GRAPH_SVG.KEY_NODE_REC_ID]: 104},{[GRAPH_SVG.KEY_NODE_OBJ_ID]: 6, [GRAPH_SVG.KEY_NODE_REC_ID]: 101}],
            [GRAPH_SVG.KEY_LINK_KEY_ID]:   105,
            [GRAPH_SVG.KEY_LINK_KEY_DATE]: '2020-01-03',
            [GRAPH_SVG.KEY_LINK_GROUP_ID]: 2,
            source: '5_104',
            target: '6_101',
        },
    ];

    this.PARENT_ID  = parent_id;
    this.PARENT_SEL = '#'+this.PARENT_ID;
    this.PARENT_JS  = document.querySelector(this.PARENT_SEL);
    this.PARENT_D3  = d3.select(this.PARENT_SEL);
    $(this.PARENT_SEL).css('overflow', 'hidden');

    this.SVG_ID     = this.html_id('svg');
    this.SVG_SEL    = '#'+this.SVG_ID;
    this.SVG_D3     = this.PARENT_D3.append('svg')
        .attr('id',                  this.SVG_ID)
        .attr('class',               'graph-svg')
        .attr('width',               '100%')
        .attr('height',              '100%')
        .attr('preserveAspectRatio', 'xMinYMin meet')
        .attr('display',             'inline-block')
        .attr('position',            'absolute')
        .attr('top',                 '0')
        .attr('left',                '0')
        .call(this.graph_zoom)
        .call(this.menu_main_ini)
        .call(this.graph_key);
    this.SVG_JS = document.querySelector(this.SVG_SEL);

    this.defs_ini();
    this.data_ini();
    this.data_update();                                         // set this.NODES_D3, this.LINKS_D3, this.NEIGHT

    this.resize(undefined);
    window.addEventListener('resize', this.resize, false);
}



// ***********************************************
// ПСЕВДОДЕСТРУКТОР - вызывать принудительно
// ***********************************************
free = function(){
    this.resize_timer_stop();
}.bind(this);


// ***********************************************
// GRAPH: TICK
// ***********************************************
graph_tick = function(){
    this.G_MAIN_D3.selectAll('.node').attr('transform', d => `translate(${d.x},${d.y})`);   // function(d) { return "translate(" + d.x + "," + d.y + ")"; }
    this.G_MAIN_D3.selectAll('.link')
        .attr("x1", function(d) {
            return d.source.x;
        })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
}.bind(this);



// ***********************************************
// GRAPH: ZOOM
// ***********************************************
graph_zoom = function(target){
    let zoom = function(event){
        this.G_MAIN_D3.attr('transform', event.transform);
    }.bind(this);

    target.call(d3.zoom().on('zoom', zoom));
    target.on('dblclick.zoom',       null);                 // отключить dbl_click приближение
}.bind(this);



// ***********************************************
// GRAPH: NODE_DRAG
// ***********************************************
graph_node_drag = function(target){
    let drag_started = function(event, d) {
        if (!event.active) this.SIMULATION.alphaTarget(0.2).alphaDecay(0.05).restart();
        d.fx = d.x;
        d.fy = d.y;
    }.bind(this);

    let drag_dragged = function(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }.bind(this);

    let drag_ended = function(event, d) {
        if (!event.active) this.SIMULATION.alphaTarget(0).alphaDecay(0.05).restart();
        // d.fx = null; d.fy = null;
    }.bind(this);

    target.call(d3.drag()
        .clickDistance(4)
        .on('start', drag_started)
        .on('drag',  drag_dragged)
        .on('end',   drag_ended)
    );
}.bind(this);





// ***********************************************
// HTML
// ***********************************************
html_id(id=''){ return this.PARENT_ID+((id!='')?('-'+id):''); }
// html_set(){
//     this.html_clear();
//     $('body').append('<section id="'+this.id_window+'" style="padding:5px;"></section>');
// }
// html_clear(){
//     if (this.jq_window) {
//         this.jq_window.parent().remove();
//         $('.window-shadow').remove();
//         $('.window-mask').remove();
//     }
// };




// ***********************************************
// RESIZE
// ***********************************************
resize = function(){
    this.resize_timer_stop();
    this.resize_timer_start();
}.bind(this);

resize_actual = function(){
    this.resize_timer_stop();

    this.width  = this.PARENT_JS.clientWidth;
    this.height = this.PARENT_JS.clientHeight;
    let margin = { top:0, left:0, bottom:0, right:0 };

    let chartWidth  = this.width  - (margin.left+margin.right);
    let chartHeight = this.height - (margin.top +margin.bottom);

    this.SIMULATION
        .force('center_force', d3.forceCenter(this.width/2, this.height/2))
        .alpha(0.3)
        .restart();
}.bind(this);

resize_timer_start = function(){
    this.resizeTimeout = setTimeout(this.resize_actual, 166);
}.bind(this);
resize_timer_stop = function(){
    if (this.resizeTimeout){
        clearTimeout(this.resizeTimeout);
        this.resizeTimeout = null;
    }
}.bind(this);

}
