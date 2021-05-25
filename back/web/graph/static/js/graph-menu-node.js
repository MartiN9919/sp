class GRAPH_MENU_NODE {

// ***********************************************
// INI
// ***********************************************
menu_node_ini = function(target){
    let cb_create_before = function(menu_struct, event, data){
        menu_struct[0].title   = (data.mark||false)?'Снять отметку':'Отметить';
        menu_struct[1].enabled = this.node_pin_clear_enabled(data);
    }.bind(this);

    this.node_menu_struct = [
        { title: 'Отметить',  icon: 'fa-check-circle', action: this.node_mark_toggle_menu },
        { title: 'Открепить', icon: 'fa-thumbtack' ,   action: this.node_pin_clear_menu },
        { type:  'separator' },
        { title: 'Удалить',   icon: 'fa-trash',        action: this.node_del_menu },
    ];
    target.on('contextmenu', d3.contextMenu(this.node_menu_struct, undefined, cb_create_before));
};

}
