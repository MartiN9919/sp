'use strict';

class Class_jstree_checked {
constructor({
    sel_parent,
    callback_checked = undefined,
    delay            = 2000,
    radio_groups     = [],
    struct_data      = [],
}) {
    this.sel_parent         = sel_parent;
    this.callback_checked   = callback_checked;
    this.delay              = delay;
    this.radio_groups       = radio_groups;
    this.tree_selected      = [];
    this.timerRefresh       = undefined;
    this.blockChange        = false;
    this.checked_timer_bind = this.checked_timer.bind(this);

    this.obj_tree = $(this.sel_parent).jstree({
        plugins  : [ 'checkbox', 'dnd' ],
        checkbox : {
            keep_selected_style: false,  // следует ли сохранить checkbox
            whole_node:          true,   // переключение check при click не только на checkbox
            tie_selection:       true,   // для отключения whole_node, отвязывает checkbox от внутренних данных
            three_state:         false,  // каскадная обработка checkbox [true]
        },
        core: {
            data: struct_data,
            expand_selected_onload: false,
            url: '/map/list/',
        },
        dnd: {
            is_draggable: function (node, e) { e.preventDefault(); return false; },     // запретить перетаскивание узлов
        },
    }).on('ready.jstree', this.ready.bind(this));
}

ready() {
    //this.obj_tree.jstree('open_all');

    // заменить иконку у развернутых по умолчанию узлов-папок
    let obj_tree_instance = this.obj_tree.jstree(true);
    this.obj_tree.jstree().get_json('#', { flat: true, }).forEach(function(item){
        if (!(item['state']['opened']||false)) return;
        if ((item['icon']||'') != 'fa fa-folder fa-md') return;
        obj_tree_instance.set_icon(item, 'fa fa-folder-open fa-md');
    });

    this.obj_tree.on('changed.jstree',    this.changed.bind(this));
    this.obj_tree.on('open_node.jstree',  this.node_open.bind(this));
    this.obj_tree.on('close_node.jstree', this.node_close.bind(this));
    this.checked_timer_bind();
}

free() {
    this.timerRefreshStop();

    this.obj_tree.off('ready.jstree');
    this.obj_tree.off('changed.jstree');
    this.obj_tree.off('open_node.jstree');
    this.obj_tree.off('close_node.jstree');

    var element = document.querySelector(this.sel_parent);
    while (element.firstChild) { element.removeChild(element.firstChild); }
}


//*********************************************************************************************
changed(e, data) {
    if (this.blockChange) return;
    if (['select_node', 'deselect_node'].indexOf(data.action) == -1) return;
    let obj_tree_instance = this.obj_tree.jstree(true);

    // нет check и есть children - развернуть/свернуть
    let obj = obj_tree_instance.get_node(data.node);
    if ((obj.state['checkbox_disabled']) && (obj.children.length>0)) {
        obj_tree_instance.toggle_node(data.node);
        return;
    }

    if (this.radio_groups.length == 0) return;
    try {
        this.blockChange  = true;   // tree_obj.off("changed.jstree"); - нельзя, так как появляется баг

        // emulate radio-button
        let item_group = data.node.id.split('.')[0];
        if (this.radio_groups.indexOf(item_group) != -1) {
            if (data.action == 'select_node'  ) {
                obj_tree_instance.get_node(data.node.parents[0]).children.forEach(function(id) {
                    if (id != data.node.id) obj_tree_instance.uncheck_node(id);
                });
            }
            if (data.action == 'deselect_node') obj_tree_instance.check_node(data.node.id);
        }
    }
    catch (e) { console.error(e); }
    finally   {
        this.blockChange = false;
        this.checked();
    }
}



//*********************************************************************************************
/**
 * CALLBACK: ИЗМЕНЕННЫЕ CHECKED
 * анализ только узлов, не имеющих дочерных элементов
*/
checked() { this.timerRefreshStart(); }
checked_timer() {
    function cmp_arr(a, b) {
        ret = [];
        a.forEach(function(item_a){
            if (b.indexOf(item_a)==-1) ret.push(item_a);
        });
        return ret;
    }

    this.timerRefresh      = undefined;
    this.tree_selected_old = this.tree_selected;
    this.tree_selected     = $(this.sel_parent).jstree("get_selected");

    // убрать узлы со скрытым cecked
    let obj_tree_instance = this.obj_tree.jstree(true);
    let i                 = this.tree_selected.length;
    let i_state           = undefined;
    while (i--) {
        i_state = obj_tree_instance.get_node(this.tree_selected[i]).state;
        if (i_state['checkbox_disabled'])
            this.tree_selected.splice(i, 1);
        //if (obj_tree_instance.get_node(this.tree_selected[i]).children.length>0) this.tree_selected.splice(i, 1);
    }

    var ret = {
        all: this.tree_selected,
        add: cmp_arr(this.tree_selected,     this.tree_selected_old),
        del: cmp_arr(this.tree_selected_old, this.tree_selected),
    };
    if ((ret.add.length!=0)||(ret.del.length!=0)) this.callback_checked(ret);
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
    this.timerRefresh = setTimeout(this.checked_timer_bind, this.delay);
}


//*********************************************************************************************
node_open (e, data) { if ((data['node']['icon']||'') == 'fa fa-folder fa-md')      data.instance.set_icon(data.node, 'fa fa-folder-open fa-md'); }
node_close(e, data) { if ((data['node']['icon']||'') == 'fa fa-folder-open fa-md') data.instance.set_icon(data.node, 'fa fa-folder fa-md'); }


}