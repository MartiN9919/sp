
class FORM_OBJ_VAL {
static COL_KEY = 'key';
static COL_VAL = 'val';
static COL_DAT = 'dat';
constructor(options) {
    this.id_parent     = options.id_parent;
    this.id_tree       = options.id_parent+'_tree';
    this.DATA          = options.data;

    this.obj_selector  = this.parent+' .panel_tree';
    this.data_obj_keys = undefined;

    this.var_menu = [
        { title: 'Найти',          icon: 'fa-search',       action: this.var_menu_search.bind(this), tip: 'Найти схожие объекты' },
        { title: 'Обновить',       icon: 'fa-sync-alt',     action: this.var_menu_refresh.bind(this) },
        { type:  'separator' },
        { title: 'Очистить',       icon: 'fa-eraser',       action: this.var_menu_clear.bind(this) },
        { title: 'Очистить все',                            action: this.var_menu_clear_all.bind(this) },
        { type:  'separator' },
        { title: 'Свернуть все',   icon: 'fa-minus-square', action: this.var_menu_collapse.bind(this) },
        { title: 'Развернуть все', icon: 'fa-plus-square',  action: this.var_menu_expand.bind(this) },
    ];
    this.VAR_MENU_CLEAR = 3;

    //this.DOM.parent.on('contextmenu', d3.contextMenu(this.var_menu, undefined, this.var_menu_open.bind(this)));
    $('#'+this.id_parent).append('<table id="'+this.id_tree+'" class="select_off" style=""></table>');   // объект не используется, но должен быть (особенность библиотеки)

    // информатор об ошибке
    //this.DOM.err = this.DOM.parent.append("p").attr("class", "mErr select_off").attr("display", "none");

    // получить список значений
    net_ajax({
        url:     INP.AJ_OBJ_VALS,
        data:    { obj_id: this.DATA.obj.id, rec_id: 1},
        success: this.refresh.bind(this),
    });


    // this.resize(undefined);
    // window.addEventListener('resize', this.resize.bind(this), false);

}

free = function() {
    //window.removeEventListener('resize', this.resize, false);
    //this.DOM = undefined;
}


refresh(data_obj_keys) {
    if (this.obj_var_tree) {
        this.obj_var_tree.free();
        this.obj_var_tree = undefined;
        delete this.obj_var_tree;
    }
    this.data_obj_keys = data_obj_keys;


    let _tree_data = [
        { id: '1', parent_id: '0', key: '4444',  val: 'dfsdfs',     dat: '5515'},
        { id: '2', parent_id: '0', key: '44434', },
        { id: '3', parent_id: '0', key: '44434', val: 'df2s222dfs', dat: '2125', },
        { id: '4', parent_id: '2', key: '44244', val: 'dfsdfs',     dat: '555', },
        { id: '5', parent_id: '0', key: '41444', val: 'dfsdf23s',   dat: '555', },
    ];

    //let tree_data = FORM_TREE.tree_child(_tree_data, 0);

    $('#'+this.id_tree).treegrid({
        idField:        'id',
        treeField:      'key',
        animate:        true,
        fit:            true,   // автоширина
        fitColumns:     true,   // автоширина
        scrollbarSize:  0,
        nowrap:         true,   // в одну строку
        singleSelect:   true,
        width:          '100%',
        height:         '100%',
        onResizeColumn: this.on_resize_col.bind(this),
        columns:[[
            { field: 'key', title: 'Ключ',     width: '30%', },
            { field: 'val', title: 'Значение', width: '50%', },
            { field: 'dat', title: 'Дата',     width: '20%', resizable: false, fixed: true, },
        ]],
        data: {
            //total:tree_data.length,
            rows: FORM_TREE.tree_add_child(_tree_data, 0),
        },
        // loadFilter: function(rows) {
        // },
    });
    $('#'+this.id_parent+' .panel-body').css('border-color', '#ffffff00');

    // this.obj_var_tree = new Class_jstree_selected({
    //     sel_parent:  this.obj_selector,
    //     grid_columns: [
    //         { header: "Ключ", },
    //         { header: "Значение", width: '100%', value: this.data_get.bind(this, 1)},
    //         { header: "Дата",     width: '10em', value: this.data_get.bind(this, 2)},
    //     ],
    //     delay:       SYS.DELAY_ACTION,
    //     struct_data: FORM_TREE.data_tree(data_obj_keys),
    // });

    // размеры
    this.on_resize();
}

on_resize_col(field, width) {
    return;
    let w = $(this.parent).outerWidth();
    let col_key = $(this.obj_selector).treegrid('getColumnOption', FORM_OBJ_VAL.COL_KEY);
    let col_val = $(this.obj_selector).treegrid('getColumnOption', FORM_OBJ_VAL.COL_VAL);
    let col_data = $(this.obj_selector).treegrid('getColumnOption', FORM_OBJ_VAL.COL_DAT);

    switch(field) {
    case FORM_OBJ_VAL.COL_KEY:
        $(this).treegrid('resizeColumn', { field: FORM_OBJ_KEY.COL_VAL, width: 200 });

    }
    // //$(this.obj_selector).treegrid('resize');
}


// получить значение узла
data_get(col, node) {
    let data_item = this.data_obj_keys.filter(v => (v.id == node.id));
    let ret = (data_item.length > 0) ? data_item.val : undefined;
    return col;

    data.instance._model.data[data.selected[0]].li_attr.class += ' newClass';
}

var_menu_open(item, data) {
    //this.var_menu[this.VAR_MENU_CLEAR].enabled = ((this.obj_var_tree.hovered_node!='') && (this.obj_var_tree.hovered_node.children.length==0));
}

var_menu_search(item, data, self) {
    let tt = 1;
    return false;
}

var_menu_refresh(item, data, self) {
    let tt = 1;
    return true;
}

var_menu_clear(item, data, self) {
    //item.enabled = (this.obj_var_tree.hovered_node.children.length>0);
}
var_menu_clear_all(item, data, self) {
    //item.enabled = (this.obj_var_tree.hovered_node.children.length>0);
}

var_menu_collapse(item, data, self) { this.obj_var_tree.obj_tree.jstree("close_all"); }
var_menu_expand  (item, data, self) { this.obj_var_tree.obj_tree.jstree("open_all" ); }


// ============================================================
// RESIZE
// ============================================================
on_resize(element) {
    //this.DOM.JS_panel_main.style.height = (document.documentElement.clientHeight-220)+'px';
    if (this.obj_var_tree) this.obj_var_tree.col_resize();
}


}