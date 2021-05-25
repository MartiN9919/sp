class FORM_OBJ_KEY {
constructor(options) {
    this.parent          = options.parent;
    this.obj_info        = options.obj_info;

    this.DOM             = {};
    this.DOM.parent      = d3.select(this.parent);
    this.DOM.panel_title = this.DOM.parent    .append("div").attr("class", "jstree-grid-header-cell jstree-grid-header-regular").text('Доступные ключи');
    this.DOM.panel_tree  = this.DOM.parent    .append("div").attr("class", "panel_tree select_off");
    this.DOM.title       = this.DOM.panel_tree.append('p')  .attr('class', 'mTitle select_off').html('<i class="fa fa-arrow fa-md"></i>555');

    // получить список ключей
    net_ajax({
        url:     AJ.SCRIPT_EXEC,
        data:    {script: AJ.SCRIPT_NAME.KEY_LIST, obj: parseInt(this.obj_info.id), },
        success: this.refresh.bind(this),
    });
}

free = function() {
    //window.removeEventListener('resize', this.resize, false);
    this.DOM = undefined;
}

refresh(data_obj_keys) {
    if (this.obj_var_tree) {
        this.obj_var_tree.free();
        this.obj_var_tree = undefined;
        delete this.obj_var_tree;
    }
    //this.DOM.panel_tree.html();

    this.data_obj_keys = data_obj_keys;

    // отобразить дерево
    this.obj_var_tree = new Class_jstree_selected({
        sel_parent:  this.parent+' .panel_tree',
        delay:       SYS.DELAY_ACTION,
        struct_data: FORM_TREE.data_tree(data_obj_keys),
    });

    // размеры
    //this.on_resize();
}

}