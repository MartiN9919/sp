'use strict';


/*  grid_columns = [                // наличие включает режим 'grid'
        { header: "Ключ" },
        { header: "Значение", width: '100%', value: this.cb_grid_val},
        { header: "Дата",     width: '100%', value: this.cb_grid_dat},
    ]
*/
class Class_jstree_selected {
constructor({
    sel_parent,
    cb_selected  = undefined,
    grid_columns = undefined,
    animation    = undefined,
    delay        = 1000,
    struct_data  = [],
}) {
    this.sel_parent          = sel_parent;
    this.cb_selected         = cb_selected;
    this.delay               = delay;
    this.tree_selected       = [];
    this.timerRefresh        = undefined;
    this.blockChange         = false;
    this.selected_timer_bind = this.selected_timer.bind(this);
    this.selected_id_old     = '';
    this.hovered_id          = '';

    let options = {
        plugins: [ 'dnd', ],
        core:    { data: struct_data, multiple: false, animation: animation || !(grid_columns), },                   // themes: { dots: false, },
        dnd:     { is_draggable: function (node, e) { e.preventDefault(); return false; }, },
    };

    // режим 'grid'
    // нужно оборачивать в div и т.п., т.к. jstree устанавливает классы для parent
    if (grid_columns) {
        options['plugins'].push('grid');
        options['grid'] = {
            columns:   grid_columns,
            width:     '100%',
            height:    '100%',
            resizable: true,
        };
    }

    this.obj_tree = $(this.sel_parent).jstree(options)
        .on('ready.jstree', this.ready.bind(this));
}


ready() {
    // заменить иконку у развернутых по умолчанию узлов-папок
    let obj_tree_instance = this.obj_tree.jstree(true);
    this.obj_tree.jstree().get_json('#', { flat: true, }).forEach(function(item){
        if (!(item['state']['opened']||false)) return;
        if ((item['icon']||'') != 'fa fa-folder fa-md') return;
        obj_tree_instance.set_icon(item, 'fa fa-folder-open fa-md');
    });

    this.obj_tree
        .on('changed.jstree',            this.changed.bind(this))
        .on('hover_node.jstree',         this.hovered.bind(this))
        .on('dehover_node.jstree',       this.dehovered.bind(this))
        .on('open_node.jstree',          this.node_open.bind(this))
        .on('close_node.jstree',         this.node_close.bind(this))
        .on('resize_column.jstree-grid', this.col_resize.bind(this))
        .on('update_cell.jstree-grid',   this.cel_update.bind(this))
        .on('select_cell.jstree-grid',   this.cel_select.bind(this));

    //$(this.sel_parent+" .jstree-ocl").hide();
    //this.selected_timer_bind();
}

free() {
    this.timerRefreshStop();

    this.obj_tree.off('ready.jstree');
    this.obj_tree.off('changed.jstree');

    var element = document.querySelector(this.sel_parent);
    while (element.firstChild) { element.removeChild(element.firstChild); }
}

//*********************************************************************************************
hovered  (e, data) { this.hovered_node = data.node; }
dehovered(e, data) { this.hovered_node = ''; }

//*********************************************************************************************
changed(e, data) {
    if (['select_node'].indexOf(data.action) == -1) return;
    this.timerRefreshStop();
    let obj_tree_instance = this.obj_tree.jstree(true);

    // не выделять папки
    if ((data.node.a_attr['class'] || '').indexOf('jstree-title')>-1) {
       this.obj_tree.jstree("deselect_node", data.node); // вызывает this.changed()
    }

    // есть children - развернуть/свернуть
    if (data.node.children.length>0) obj_tree_instance.toggle_node(data.node);

    this.selected();
}


//*********************************************************************************************
selected() { this.timerRefreshStart(); }
selected_timer() {
    // id выделенного узла (для папок = '')
    let selected_id_new = this.obj_tree.jstree().get_selected();
    if (selected_id_new.length>0) {
        selected_id_new = selected_id_new[0];
        let selected_node   = this.obj_tree.jstree(true).get_node(selected_id_new);
        if ((selected_node.a_attr['class'] || '').indexOf('jstree-title')>-1) selected_id_new='';
    } else {
        selected_id_new = '';
    }
    if (selected_id_new===this.selected_id_old) return;

    let ret  = {
        'new': selected_id_new,
        'old': this.selected_id_old,
    };
    this.selected_id_old = selected_id_new;
    if (this.cb_selected) this.cb_selected(ret);
}


//*********************************************************************************************
timerRefreshStop() {
    if (this.timerRefresh) {
        clearTimeout(this.timerRefresh);
        this.timerRefresh = undefined;
    }
}

timerRefreshStart() {
    this.timerRefreshStop();
    this.timerRefresh = setTimeout(this.selected_timer_bind, this.delay);
}


//*********************************************************************************************
node_open (e, data) { if ((data['node']['icon']||'') == 'fa fa-folder fa-md')      data.instance.set_icon(data.node, 'fa fa-folder-open fa-md'); }
node_close(e, data) { if ((data['node']['icon']||'') == 'fa fa-folder-open fa-md') data.instance.set_icon(data.node, 'fa fa-folder fa-md'); }
col_resize(e, col, width) {
    let obj_parent = $(this.sel_parent);
    let obj_col_0  = $(this.sel_parent+' .jstree-grid-column-0');
    let obj_col_1  = $(this.sel_parent+' .jstree-grid-column-1');
    let obj_col_2  = $(this.sel_parent+' .jstree-grid-column-2');
    let width_new  = obj_parent.width() - ((width)?width:0);

    if (col==1) {
        width_new -= (obj_col_2.width()+1);
        obj_col_0.width(width_new).css('max-width', width_new).css('min-width', width_new);
        return;
    }

    if (col==0)         { width_new -= obj_col_2.width(); }
    if (col==2)         { width_new -= obj_col_0.width(); }
    if (col==undefined) { width_new -= obj_col_0.width() - obj_col_2.width(); }
    obj_col_1.width(width_new).css('max-width', 'None').css('min-width', 'None');
}

cel_update(e, col, width) {
    let tt=1;
}

cel_select(e, data, rr, yy, uu, ii) {
    //e.preventDefault();
    var tree = this.obj_tree.jstree(true); //$(this.sel_parent).jstree(true);
    // tree.edit(data.node); нет ошибки и нет результата
    // this.obj_tree.jstree('edit', data.node); нет ошибки и нет результата
    // tree._edit(data.node, 2); нет ошибки и нет результата
    tree.edit(data.node, 2);
    return;
    //var node = tree.get_node(data.node);
    //tree.edit(data.node);

    //this.obj_tree.jstree('open_all');
    this.obj_tree.jstree('edit', node);
    return;

    //var nodeToEdit = $(this.sel_parent).jstree().get_selected();
    $(this.sel_parent).jstree('edit', this.hovered_node);
    return;

    var dd = $(this.sel_parent).jstree();
    let q = this.obj_tree;
    dd.edit(this.hovered_node);

    /*
var tree = $("#jstree").jstree(true), node = tree.get_node("my_node");
node.data.value = 25;
tree.trigger("change_node.jstree",node);
    */
}

}
